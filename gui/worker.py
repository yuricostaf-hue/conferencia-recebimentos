"""Background worker for PDF processing."""

from pathlib import Path
from typing import Callable, Optional

from core.logger import ApplicationLogger
from core.agenda_parser import AgendaParser
from core.demonstrativo_parser import DemonstrativoParser
from core.matcher import Matcher
from core.pdf_marker import PDFMarker
from core.reporter import Reporter


class ProcessingWorker:
    """Background worker for processing PDFs."""

    def __init__(
        self,
        agendas_dir: Path,
        demonstrativos_dir: Path,
        output_dir: Path,
        log_callback: Callable[[str], None],
        progress_callback: Callable[[float, int, int, int], None],
        complete_callback: Callable[[bool], None],
    ) -> None:
        """Initialize the worker.

        Args:
            agendas_dir: Directory with agenda PDFs.
            demonstrativos_dir: Directory with payment statement PDFs.
            output_dir: Output directory for results.
            log_callback: Callback for log messages.
            progress_callback: Callback for progress updates.
            complete_callback: Callback for completion.
        """
        self.agendas_dir = agendas_dir
        self.demonstrativos_dir = demonstrativos_dir
        self.output_dir = output_dir
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback

        self.logger = ApplicationLogger(output_dir)
        self.agenda_parser = AgendaParser(self.logger)
        self.demonstrativo_parser = DemonstrativoParser(self.logger)
        self.matcher = Matcher(self.logger)
        self.pdf_marker = PDFMarker(self.logger)
        self.reporter = Reporter(self.logger)

    def run(self) -> None:
        """Run the processing workflow."""
        try:
            self.log_callback("Iniciando processamento...")

            # Parse agendas
            self.log_callback("Lendo agendas...")
            agenda_entries = self.agenda_parser.parse_directory(self.agendas_dir)
            self.log_callback(f"Encontradas {len(agenda_entries)} entradas em agendas")
            self.progress_callback(0.2, 0, len(set(e.paciente for e in agenda_entries)), 0)

            # Parse demonstrativos
            self.log_callback("Lendo demonstrativos...")
            payment_entries = self.demonstrativo_parser.parse_directory(
                self.demonstrativos_dir
            )
            self.log_callback(f"Encontradas {len(payment_entries)} entradas de pagamento")
            self.progress_callback(0.4, 0, 0, 0)

            # Match entries
            self.log_callback("Comparando entradas...")
            match_results = self.matcher.match_entries(agenda_entries, payment_entries)
            paid_count = sum(1 for r in match_results if r.is_paid)
            self.log_callback(f"Encontradas {paid_count} correspondências")
            self.progress_callback(0.6, 0, 0, paid_count)

            # Mark PDFs
            self.log_callback("Marcando PDFs...")
            marked_dir = self.output_dir / "Agendas Conferidas"
            for agenda_file in self.agendas_dir.glob("*.pdf"):
                file_results = [r for r in match_results if r.agenda_entry.arquivo == agenda_file.name]
                output_file = marked_dir / agenda_file.name
                self.pdf_marker.mark_pdf(agenda_file, output_file, file_results)
            self.progress_callback(0.8, len(list(self.agendas_dir.glob("*.pdf"))), 0, paid_count)

            # Generate reports
            self.log_callback("Gerando relatórios...")
            self.reporter.generate_results_report(
                match_results, self.output_dir / "resultado.xlsx"
            )

            not_found = [
                p for p in payment_entries
                if not any(
                    r.payment_entry == p and r.is_paid
                    for r in match_results
                )
            ]
            self.reporter.generate_not_found_report(
                not_found, self.output_dir / "nao_encontrados.xlsx"
            )
            self.progress_callback(1.0, 0, 0, paid_count)

            self.log_callback("Processamento concluído com sucesso!")
            self.complete_callback(True)

        except Exception as e:
            self.logger.error(f"Erro durante processamento: {str(e)}")
            self.log_callback(f"Erro: {str(e)}")
            self.complete_callback(False)

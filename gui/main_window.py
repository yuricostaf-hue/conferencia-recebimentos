"""Main application window."""

import os
import threading
from pathlib import Path
from typing import Optional, Callable

import customtkinter as ctk
from tkinter import filedialog, messagebox

from .settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_NORMAL,
    FONT_SMALL,
    PADDING_LARGE,
    PADDING_MEDIUM,
    PADDING_SMALL,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    COLOR_SUCCESS,
    COLOR_TEXT,
)
from .worker import ProcessingWorker


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)

        self.agendas_dir: Optional[Path] = None
        self.demonstrativos_dir: Optional[Path] = None
        self.output_dir: Optional[Path] = None

        self.worker: Optional[ProcessingWorker] = None
        self.processing = False

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLOR_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Conferência de Recebimentos",
            font=FONT_TITLE,
            text_color=COLOR_TEXT,
        )
        title_label.pack(pady=PADDING_LARGE)

        # Input section
        input_frame = self._create_input_section(main_frame)
        input_frame.pack(fill="x", padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        # Processing section
        processing_frame = self._create_processing_section(main_frame)
        processing_frame.pack(fill="both", expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        # Button section
        button_frame = self._create_button_section(main_frame)
        button_frame.pack(fill="x", padx=PADDING_LARGE, pady=PADDING_LARGE)

    def _create_input_section(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create input folder selection section."""
        frame = ctk.CTkFrame(parent, fg_color=COLOR_SECONDARY)
        frame.pack_propagate(False)

        # Agendas
        agendas_label = ctk.CTkLabel(
            frame, text="Pasta das Agendas:", font=FONT_NORMAL, text_color=COLOR_TEXT
        )
        agendas_label.grid(row=0, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.agendas_button = ctk.CTkButton(
            frame,
            text="Selecionar Pasta",
            command=self._select_agendas_dir,
            font=FONT_SMALL,
        )
        self.agendas_button.grid(row=0, column=1, sticky="ew", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.agendas_label = ctk.CTkLabel(
            frame,
            text="Nenhuma pasta selecionada",
            font=FONT_SMALL,
            text_color="#a0a0a0",
        )
        self.agendas_label.grid(row=0, column=2, sticky="w", padx=PADDING_SMALL)

        # Demonstrativos
        demo_label = ctk.CTkLabel(
            frame,
            text="Pasta dos Demonstrativos:",
            font=FONT_NORMAL,
            text_color=COLOR_TEXT,
        )
        demo_label.grid(row=1, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.demo_button = ctk.CTkButton(
            frame,
            text="Selecionar Pasta",
            command=self._select_demonstrativos_dir,
            font=FONT_SMALL,
        )
        self.demo_button.grid(row=1, column=1, sticky="ew", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.demo_label = ctk.CTkLabel(
            frame,
            text="Nenhuma pasta selecionada",
            font=FONT_SMALL,
            text_color="#a0a0a0",
        )
        self.demo_label.grid(row=1, column=2, sticky="w", padx=PADDING_SMALL)

        # Output
        output_label = ctk.CTkLabel(
            frame, text="Pasta de Saída:", font=FONT_NORMAL, text_color=COLOR_TEXT
        )
        output_label.grid(row=2, column=0, sticky="w", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.output_button = ctk.CTkButton(
            frame,
            text="Selecionar Pasta",
            command=self._select_output_dir,
            font=FONT_SMALL,
        )
        self.output_button.grid(row=2, column=1, sticky="ew", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.output_label = ctk.CTkLabel(
            frame,
            text="Nenhuma pasta selecionada",
            font=FONT_SMALL,
            text_color="#a0a0a0",
        )
        self.output_label.grid(row=2, column=2, sticky="w", padx=PADDING_SMALL)

        frame.columnconfigure(1, weight=1)
        return frame

    def _create_processing_section(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create processing status section."""
        frame = ctk.CTkFrame(parent, fg_color=COLOR_SECONDARY)

        # Progress bar
        progress_label = ctk.CTkLabel(
            frame, text="Progresso:", font=FONT_SMALL, text_color=COLOR_TEXT
        )
        progress_label.pack(anchor="w", padx=PADDING_SMALL, pady=(PADDING_SMALL, 5))

        self.progress_bar = ctk.CTkProgressBar(frame, height=20)
        self.progress_bar.pack(fill="x", padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.progress_bar.set(0)

        # Stats frame
        stats_frame = ctk.CTkFrame(frame, fg_color=COLOR_PRIMARY)
        stats_frame.pack(fill="x", padx=PADDING_SMALL, pady=PADDING_SMALL)

        self.pdfs_label = ctk.CTkLabel(
            stats_frame,
            text="PDFs processados: 0",
            font=FONT_SMALL,
            text_color=COLOR_TEXT,
        )
        self.pdfs_label.pack(anchor="w", padx=PADDING_SMALL, pady=5)

        self.patients_label = ctk.CTkLabel(
            stats_frame,
            text="Pacientes encontrados: 0",
            font=FONT_SMALL,
            text_color=COLOR_TEXT,
        )
        self.patients_label.pack(anchor="w", padx=PADDING_SMALL, pady=5)

        self.procedures_label = ctk.CTkLabel(
            stats_frame,
            text="Procedimentos pagos: 0",
            font=FONT_SMALL,
            text_color=COLOR_TEXT,
        )
        self.procedures_label.pack(anchor="w", padx=PADDING_SMALL, pady=5)

        # Log text
        log_label = ctk.CTkLabel(
            frame, text="Log:", font=FONT_SMALL, text_color=COLOR_TEXT
        )
        log_label.pack(anchor="w", padx=PADDING_SMALL, pady=(PADDING_SMALL, 5))

        self.log_text = ctk.CTkTextbox(
            frame, height=150, font=FONT_SMALL, text_color=COLOR_TEXT
        )
        self.log_text.pack(fill="both", expand=True, padx=PADDING_SMALL, pady=PADDING_SMALL)
        self.log_text.configure(state="disabled")

        return frame

    def _create_button_section(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create button section."""
        frame = ctk.CTkFrame(parent, fg_color=COLOR_PRIMARY)

        self.process_button = ctk.CTkButton(
            frame,
            text="PROCESSAR",
            command=self._start_processing,
            font=FONT_SUBTITLE,
            height=40,
            fg_color=COLOR_ACCENT,
        )
        self.process_button.pack(side="left", fill="x", expand=True, padx=(0, PADDING_SMALL))

        self.open_output_button = ctk.CTkButton(
            frame,
            text="Abrir Pasta",
            command=self._open_output_folder,
            font=FONT_SMALL,
            height=40,
            state="disabled",
        )
        self.open_output_button.pack(side="left", fill="x", expand=True)

        return frame

    def _select_agendas_dir(self) -> None:
        """Select agendas directory."""
        directory = filedialog.askdirectory(title="Selecione a pasta das agendas")
        if directory:
            self.agendas_dir = Path(directory)
            self.agendas_label.configure(text=self.agendas_dir.name)

    def _select_demonstrativos_dir(self) -> None:
        """Select demonstrativos directory."""
        directory = filedialog.askdirectory(title="Selecione a pasta dos demonstrativos")
        if directory:
            self.demonstrativos_dir = Path(directory)
            self.demo_label.configure(text=self.demonstrativos_dir.name)

    def _select_output_dir(self) -> None:
        """Select output directory."""
        directory = filedialog.askdirectory(title="Selecione a pasta de saída")
        if directory:
            self.output_dir = Path(directory)
            self.output_label.configure(text=self.output_dir.name)

    def _start_processing(self) -> None:
        """Start the processing."""
        if not self.agendas_dir or not self.demonstrativos_dir or not self.output_dir:
            messagebox.showerror(
                "Erro", "Por favor, selecione todas as pastas antes de processar."
            )
            return

        if self.processing:
            messagebox.showwarning("Aviso", "Um processamento já está em andamento.")
            return

        self.processing = True
        self.process_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.worker = ProcessingWorker(
            self.agendas_dir,
            self.demonstrativos_dir,
            self.output_dir,
            self._on_log_message,
            self._on_progress_update,
            self._on_processing_complete,
        )

        thread = threading.Thread(target=self.worker.run, daemon=True)
        thread.start()

    def _on_log_message(self, message: str) -> None:
        """Handle log message from worker."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _on_progress_update(
        self,
        progress: float,
        pdfs: int,
        patients: int,
        procedures: int,
    ) -> None:
        """Handle progress update from worker."""
        self.progress_bar.set(progress)
        self.pdfs_label.configure(text=f"PDFs processados: {pdfs}")
        self.patients_label.configure(text=f"Pacientes encontrados: {patients}")
        self.procedures_label.configure(text=f"Procedimentos pagos: {procedures}")

    def _on_processing_complete(self, success: bool) -> None:
        """Handle processing completion."""
        self.processing = False
        self.process_button.configure(state="normal")
        self.open_output_button.configure(state="normal")

        if success:
            messagebox.showinfo("Sucesso", "A conferência foi concluída.")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro durante o processamento.")

    def _open_output_folder(self) -> None:
        """Open the output folder."""
        if self.output_dir and self.output_dir.exists():
            os.startfile(str(self.output_dir))

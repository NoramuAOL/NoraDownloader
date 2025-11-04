# -*- coding: utf-8 -*-
"""Spotify Downloader Module - Wrapper for spotdl"""

import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

console = Console()


class SpotifyDownloader:
    """Spotify downloader wrapper"""
    
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def check_spotdl(self) -> bool:
        """Check if spotdl is installed"""
        try:
            result = subprocess.run(
                ["spotdl", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_spotdl(self):
        """Install spotdl"""
        console.print("\n[yellow]spotdl bulunamadi. Yukleniyor...[/yellow]")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "spotdl"],
                check=True,
                capture_output=True
            )
            console.print("[green]OK[/green] spotdl basariyla yuklendi!\n")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]X[/red] spotdl yuklenemedi: {e}\n")
            return False
    
    def interactive_mode_with_url(self, url: str):
        """Interactive mode with pre-provided URL"""
        # Bitrate selection
        bitrate_table = Table(show_header=True, box=box.SIMPLE)
        bitrate_table.add_column("Secenek", style="cyan", justify="center")
        bitrate_table.add_column("Aciklama", style="white")
        bitrate_table.add_row("1", "En Iyi Kalite (320kbps)")
        bitrate_table.add_row("2", "Yuksek Kalite (256kbps)")
        bitrate_table.add_row("3", "Normal Kalite (192kbps)")
        bitrate_table.add_row("4", "Dusuk Kalite (128kbps)")
        
        console.print(bitrate_table)
        bitrate_choice = Prompt.ask(
            "[yellow]Kalite secin[/yellow]",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        bitrate_map = {"1": "320k", "2": "256k", "3": "192k", "4": "128k"}
        bitrate = bitrate_map[bitrate_choice]
        
        # Format selection
        format_table = Table(show_header=True, box=box.SIMPLE)
        format_table.add_column("Secenek", style="cyan", justify="center")
        format_table.add_column("Format", style="white")
        format_table.add_row("1", "MP3 (Onerilen)")
        format_table.add_row("2", "M4A")
        format_table.add_row("3", "FLAC (Kayipsiz)")
        
        console.print(format_table)
        format_choice = Prompt.ask(
            "[yellow]Format secin[/yellow]",
            choices=["1", "2", "3"],
            default="1"
        )
        format_map = {"1": "mp3", "2": "m4a", "3": "flac"}
        format_type = format_map[format_choice]
        
        # Custom output directory
        custom_dir = Confirm.ask(
            "[yellow]Ozel cikti dizini kullanmak ister misiniz?[/yellow]",
            default=False
        )
        
        if custom_dir:
            output_dir = Prompt.ask(
                "[yellow]Cikti dizini[/yellow]",
                default=str(self.output_dir)
            )
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(exist_ok=True)
        
        console.print()
        self.download(url, bitrate, format_type)
    
    def download(self, url: str, bitrate: str = "320k", format: str = "mp3"):
        """Download from Spotify with optimizations"""
        cmd = [
            "spotdl",
            "download",
            url,
            "--output", str(self.output_dir),
            "--format", format,
            "--bitrate", bitrate,
            "--threads", "4",  # 4 paralel indirme
            "--cookie-file", "",  # Cookie kullanma (daha hızlı)
        ]
        
        console.print(f"[bold green]→[/bold green] Hizli indirme baslatiliyor (4 paralel)...\n")
        
        try:
            subprocess.run(cmd, check=True)
            console.print(f"\n[bold green]OK Indirme tamamlandi![/bold green]")
            console.print(f"[cyan]Konum: {self.output_dir}[/cyan]")
        except subprocess.CalledProcessError as e:
            console.print(f"\n[bold red]X Indirme sirasinda hata olustu![/bold red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Indirme iptal edildi.[/yellow]")

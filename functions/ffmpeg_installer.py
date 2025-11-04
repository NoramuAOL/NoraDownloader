# -*- coding: utf-8 -*-
"""FFmpeg Automatic Installer"""

import subprocess
import sys
import os
import platform
import zipfile
import requests
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn

console = Console()


class FFmpegInstaller:
    """FFmpeg otomatik kurulum yöneticisi"""
    
    def __init__(self):
        self.system = platform.system()
        self.ffmpeg_dir = Path.home() / ".noradownloader" / "ffmpeg"
        self.ffmpeg_dir.mkdir(parents=True, exist_ok=True)
    
    def check_ffmpeg(self) -> bool:
        """FFmpeg'in yüklü olup olmadığını kontrol et"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ffmpeg_windows(self):
        """Windows için FFmpeg kur"""
        console.print("[cyan]→ Windows icin FFmpeg kuruluyor...[/cyan]\n")
        
        # Önce winget dene
        console.print("[dim]winget ile deneniyor...[/dim]")
        try:
            result = subprocess.run(
                ["winget", "install", "FFmpeg", "--silent"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                console.print("[green]✓ FFmpeg winget ile kuruldu![/green]\n")
                return True
        except:
            pass
        
        console.print("[yellow]winget basarisiz, manuel indirme yapiliyor...[/yellow]\n")
        
        # Manuel indirme
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        zip_path = self.ffmpeg_dir / "ffmpeg.zip"
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                console=console
            ) as progress:
                task = progress.add_task("FFmpeg indiriliyor...", total=None)
                
                response = requests.get(url, stream=True, timeout=60)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                progress.update(task, total=total_size)
                
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
            
            console.print("[cyan]Dosyalar cikartiliyor...[/cyan]")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.ffmpeg_dir)
            
            # ffmpeg.exe bul
            for root, dirs, files in os.walk(self.ffmpeg_dir):
                if 'ffmpeg.exe' in files:
                    ffmpeg_bin = Path(root)
                    os.environ['PATH'] = str(ffmpeg_bin) + os.pathsep + os.environ['PATH']
                    
                    console.print(f"[green]✓ FFmpeg kuruldu: {ffmpeg_bin}[/green]")
                    console.print(f"[yellow]Not: Bu oturum icin gecerli[/yellow]\n")
                    
                    if zip_path.exists():
                        zip_path.unlink()
                    return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]✗ Hata: {str(e)[:80]}[/red]")
            console.print("[yellow]Manuel kurulum:[/yellow] winget install FFmpeg\n")
            return False
    
    def install_ffmpeg_linux(self):
        """Linux için FFmpeg kur"""
        console.print("[cyan]→ Linux icin FFmpeg kuruluyor...[/cyan]\n")
        
        try:
            result = subprocess.run(
                ["sudo", "apt-get", "install", "-y", "ffmpeg"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✓ FFmpeg kuruldu![/green]\n")
                return True
            
            result = subprocess.run(
                ["sudo", "dnf", "install", "-y", "ffmpeg"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✓ FFmpeg kuruldu![/green]\n")
                return True
            
            console.print("[red]✗ FFmpeg kurulamadi[/red]")
            console.print("[yellow]Manuel: sudo apt install ffmpeg[/yellow]\n")
            return False
            
        except Exception as e:
            console.print(f"[red]✗ Hata: {e}[/red]\n")
            return False
    
    def install_ffmpeg_mac(self):
        """macOS için FFmpeg kur"""
        console.print("[cyan]→ macOS icin FFmpeg kuruluyor...[/cyan]\n")
        
        try:
            result = subprocess.run(
                ["brew", "install", "ffmpeg"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✓ FFmpeg kuruldu![/green]\n")
                return True
            else:
                console.print("[red]✗ FFmpeg kurulamadi[/red]")
                console.print("[yellow]Homebrew yuklu mu?[/yellow]\n")
                return False
                
        except Exception as e:
            console.print(f"[red]✗ Hata: {e}[/red]\n")
            return False
    
    def install(self):
        """Platform'a göre FFmpeg kur"""
        if self.check_ffmpeg():
            console.print("[green]✓ FFmpeg zaten yuklu![/green]\n")
            return True
        
        success = False
        if self.system == "Windows":
            success = self.install_ffmpeg_windows()
        elif self.system == "Linux":
            success = self.install_ffmpeg_linux()
        elif self.system == "Darwin":
            success = self.install_ffmpeg_mac()
        else:
            console.print(f"[red]✗ Desteklenmeyen platform: {self.system}[/red]\n")
            return False
        
        if success and self.check_ffmpeg():
            console.print("[green]✓ FFmpeg basariyla kuruldu ve test edildi![/green]\n")
            return True
        elif success:
            console.print("[yellow]⚠ FFmpeg kuruldu ama test edilemedi[/yellow]")
            console.print("[dim]Terminal'i yeniden baslatmaniz gerekebilir[/dim]\n")
            return True
        
        return False

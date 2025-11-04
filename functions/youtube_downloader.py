# -*- coding: utf-8 -*-
"""YouTube Downloader Module - Wrapper for yt-dlp"""

import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

console = Console()


class YouTubeDownloader:
    """YouTube downloader wrapper"""
    
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def check_ytdlp(self) -> bool:
        """Check if yt-dlp is installed"""
        try:
            result = subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ytdlp(self):
        """Install yt-dlp"""
        console.print("\n[yellow]yt-dlp bulunamadi. Yukleniyor...[/yellow]")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                check=True,
                capture_output=True
            )
            console.print("[green]OK[/green] yt-dlp basariyla yuklendi!\n")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]X[/red] yt-dlp yuklenemedi: {e}\n")
            return False
    
    def update_ytdlp(self):
        """Update yt-dlp to latest version"""
        console.print("[yellow]yt-dlp guncelleniyor...[/yellow]")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                check=True,
                capture_output=True
            )
            console.print("[green]OK[/green] yt-dlp guncellendi!\n")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]X[/red] yt-dlp guncellenemedi: {e}\n")
            return False
    
    def interactive_mode_with_url(self, url: str):
        """Interactive mode with pre-provided URL"""
        # Audio only?
        audio_only = Confirm.ask(
            "[yellow]Sadece ses olarak indir (MP3)?[/yellow]",
            default=False
        )
        
        if not audio_only:
            # Quality selection
            quality_table = Table(show_header=True, box=box.SIMPLE)
            quality_table.add_column("Secenek", style="cyan", justify="center")
            quality_table.add_column("Aciklama", style="white")
            quality_table.add_row("1", "En Iyi Kalite (1080p+)")
            quality_table.add_row("2", "Yuksek Kalite (720p)")
            quality_table.add_row("3", "Normal Kalite (480p)")
            
            console.print(quality_table)
            quality_choice = Prompt.ask(
                "[yellow]Kalite secin[/yellow]",
                choices=["1", "2", "3"],
                default="1"
            )
            quality_map = {"1": "best", "2": "720", "3": "480"}
            quality = quality_map[quality_choice]
            
            # Format selection
            format_table = Table(show_header=True, box=box.SIMPLE)
            format_table.add_column("Secenek", style="cyan", justify="center")
            format_table.add_column("Format", style="white")
            format_table.add_row("1", "MP4 (Onerilen)")
            format_table.add_row("2", "MKV")
            format_table.add_row("3", "WEBM")
            
            console.print(format_table)
            format_choice = Prompt.ask(
                "[yellow]Format secin[/yellow]",
                choices=["1", "2", "3"],
                default="1"
            )
            format_map = {"1": "mp4", "2": "mkv", "3": "webm"}
            format_type = format_map[format_choice]
        else:
            quality = "best"
            format_type = "mp3"
        
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
        self.download(url, quality, format_type, audio_only)
    
    def download(self, url: str, quality: str = "best", format: str = "mp4", audio_only: bool = False):
        """Download from YouTube with optimizations and metadata"""
        base_cmd = [
            "yt-dlp",
            "--concurrent-fragments", "4",  # 4 paralel parça indirme
            "--no-mtime",  # Daha hızlı
            "--no-playlist" if "playlist" not in url.lower() else "--yes-playlist",
            "--extractor-args", "youtube:player_client=android,web",  # SABR sorununu çöz
            "--no-warnings",  # Uyarıları gizle
            "--quiet",  # Sessiz mod
            "--progress",  # Sadece ilerleme göster
            # Metadata ayarları
            "--embed-metadata",  # Metadata'yı dosyaya göm
            "--embed-thumbnail",  # Thumbnail'i göm
            "--convert-thumbnails", "jpg",  # Thumbnail'i jpg'ye çevir
            "--add-metadata",  # Ek metadata ekle
            "--parse-metadata", "title:%(title)s",  # Başlık
            "--parse-metadata", "uploader:%(artist)s",  # Sanatçı (uploader)
            "-o", str(self.output_dir / "%(title)s.%(ext)s"),
        ]
        
        if audio_only:
            cmd = base_cmd + [
                "-x",  # Extract audio
                "--audio-format", "mp3",
                "--audio-quality", "0",  # Best quality
                "--embed-thumbnail",  # MP3'e thumbnail ekle
                "--metadata-from-title", "%(artist)s - %(title)s",  # Başlıktan metadata çıkar
                url
            ]
        else:
            cmd = base_cmd + [
                "-f", f"bestvideo[ext={format}]+bestaudio/best[ext={format}]/best",
                "--merge-output-format", format,
                url
            ]
        
        console.print(f"[bold green]→[/bold green] Hizli indirme baslatiliyor (4 paralel + metadata)...\n")
        
        try:
            subprocess.run(cmd, check=True)
            console.print(f"\n[bold green]OK Indirme tamamlandi![/bold green]")
            console.print(f"[cyan]Konum: {self.output_dir}[/cyan]")
            
            # İndirilen dosyaları göster ve metadata kontrol et
            self.show_downloaded_files(audio_only)
            
        except subprocess.CalledProcessError as e:
            console.print(f"\n[bold red]X Indirme sirasinda hata olustu![/bold red]")
            console.print(f"[dim]yt-dlp'yi guncelleyin: pip install --upgrade yt-dlp[/dim]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Indirme iptal edildi.[/yellow]")
    
    def show_downloaded_files(self, audio_only: bool = False):
        """İndirilen dosyaları ve metadata'larını göster"""
        import json
        from rich.table import Table
        from rich import box
        
        # Son indirilen dosyaları bul
        extensions = ['mp3'] if audio_only else ['mp4', 'mkv', 'webm']
        files = []
        for ext in extensions:
            files.extend(list(self.output_dir.glob(f"*.{ext}")))
        
        if not files:
            return
        
        # En son değiştirilen 5 dosyayı al
        recent_files = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        
        console.print("\n[bold cyan]Indirilen Dosyalar:[/bold cyan]")
        
        for file_path in recent_files:
            # Dosya bilgileri
            size_bytes = file_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            console.print(f"\n[green]✓[/green] [white]{file_path.name}[/white]")
            console.print(f"  [dim]Boyut:[/dim] [yellow]{size_mb:.2f} MB[/yellow]")
            
            # Metadata'yı ffprobe ile al
            try:
                cmd = [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    str(file_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    
                    if 'format' in data and 'tags' in data['format']:
                        tags = data['format']['tags']
                        
                        # Metadata bilgilerini göster
                        metadata_parts = []
                        
                        # Başlık
                        title = tags.get('title', tags.get('TITLE', ''))
                        if title:
                            metadata_parts.append(f"[dim cyan]Baslik:[/dim cyan] [white]{title[:40]}[/white]")
                        
                        # Sanatçı/Uploader
                        artist = tags.get('artist', tags.get('ARTIST', tags.get('uploader', tags.get('UPLOADER', ''))))
                        if artist:
                            metadata_parts.append(f"[dim cyan]Sanatci:[/dim cyan] [white]{artist[:40]}[/white]")
                        
                        # Süre
                        if 'duration' in data['format']:
                            duration = float(data['format']['duration'])
                            mins = int(duration // 60)
                            secs = int(duration % 60)
                            metadata_parts.append(f"[dim cyan]Sure:[/dim cyan] [white]{mins}:{secs:02d}[/white]")
                        
                        # Bitrate
                        if 'bit_rate' in data['format']:
                            bitrate = int(data['format']['bit_rate']) // 1000
                            metadata_parts.append(f"[dim cyan]Bitrate:[/dim cyan] [white]{bitrate} kbps[/white]")
                        
                        # Metadata'yı yazdır
                        if metadata_parts:
                            for i in range(0, len(metadata_parts), 2):
                                line_parts = metadata_parts[i:i+2]
                                console.print("  " + " [dim]|[/dim] ".join(line_parts))
                    
            except Exception:
                # Metadata alınamazsa sessizce devam et
                pass
        
        console.print()

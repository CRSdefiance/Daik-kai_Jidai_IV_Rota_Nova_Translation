from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class RomDependencyError(RuntimeError):
    pass


def _ndspy_rom():
    try:
        from ndspy import rom
    except ImportError as error:
        raise RomDependencyError("ndspy is required; install the project dependencies") from error
    return rom


def _text(value: bytes) -> str:
    return value.rstrip(b"\0 ").decode("ascii", errors="replace")


@dataclass
class NdsImage:
    source: Path
    rom: object

    @classmethod
    def open(cls, path: str | Path) -> NdsImage:
        source = Path(path)
        return cls(source, _ndspy_rom().NintendoDSRom.fromFile(str(source)))

    @property
    def files(self) -> list[bytes]:
        return self.rom.files

    def metadata(self) -> dict[str, object]:
        return {
            "path": str(self.source),
            "size_bytes": self.source.stat().st_size,
            "game_title": _text(self.rom.name),
            "game_code": _text(self.rom.idCode),
            "maker_code": _text(self.rom.developerCode),
            "file_count": len(self.files),
        }

    def iter_files(self) -> Iterator[tuple[int, str, bytes]]:
        seen: set[int] = set()

        def walk(folder: object, prefix: PurePosixPath) -> Iterator[tuple[int, str, bytes]]:
            for index, name in enumerate(folder.files):
                file_id = folder.firstID + index
                seen.add(file_id)
                yield file_id, "/" + str(prefix / name), bytes(self.files[file_id])
            for name, child in folder.folders:
                yield from walk(child, prefix / name)

        yield from walk(self.rom.filenames, PurePosixPath())
        for file_id, data in enumerate(self.files):
            if file_id not in seen:
                yield file_id, f"/__unnamed__/file_{file_id:05d}.bin", bytes(data)

    def path_map(self) -> dict[str, int]:
        return {path: file_id for file_id, path, _ in self.iter_files()}

    def iter_components(self) -> Iterator[tuple[str, bytes]]:
        yield "/__arm9__.bin", bytes(self.rom.arm9)
        yield "/__arm7__.bin", bytes(self.rom.arm7)

    def read_file(self, path: str) -> bytes:
        if path == "/__arm9__.bin":
            return bytes(self.rom.arm9)
        if path == "/__arm7__.bin":
            return bytes(self.rom.arm7)
        try:
            return bytes(self.files[self.path_map()[path]])
        except KeyError as error:
            raise KeyError(f"ROM file or component not found: {path}") from error

    def replace_file(self, path: str, data: bytes) -> None:
        if path == "/__arm9__.bin":
            self.rom.arm9 = bytearray(data)
            return
        if path == "/__arm7__.bin":
            self.rom.arm7 = bytearray(data)
            return
        try:
            file_id = self.path_map()[path]
        except KeyError as error:
            raise KeyError(f"ROM file not found: {path}") from error
        self.rom.files[file_id] = data

    def save(self, output: str | Path) -> None:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.rom.saveToFile(str(destination))

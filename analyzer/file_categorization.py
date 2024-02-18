from collections import defaultdict
from os import stat
from pathlib import Path
from typing import DefaultDict, Dict, Union

from bitmath import NIST, Byte
from rich.console import Console
from rich.table import Table


def convert_size(size: int, target_unit: str) -> str:
    """
    Convert a given size in bytes to the best fitting unit.

    Parameters:
    - size (int): The size in bytes to be converted.
    - target_unit (str): The unit to which the size should be converted.

    Returns:
    str: A string representation of the size in the target unit, rounded to two decimal places.
    """
    size_in_bytes = Byte(size)
    converted_size = size_in_bytes.best_prefix(system=NIST)
    converted_size_str = "{:.2f} {}".format(converted_size.value, target_unit)
    return converted_size_str


class FileCategorization:
    category_mapping: Dict[str, set] = {
        "Text": {
            ".doc",
            ".docx",
            ".docm",
            ".odt",
            ".pdf",
            ".txt",
            ".rtf",
            ".pages",
            ".pfb",
            ".mobi",
            ".chm",
            ".tex",
            ".bib",
            ".dvi",
            ".abw",
            ".text",
            ".epub",
            ".nfo",
            ".log",
            ".log1",
            ".log2",
            ".wks",
            ".wps",
            ".wpd",
            ".emlx",
            ".utf8",
            ".ichat",
            ".asc",
            ".ott",
            ".fra",
            ".opf",
        },
        "Image": {
            ".img",
            ".jpg",
            ".jpeg",
            ".png",
            ".png0",
            ".ai",
            ".cr2",
            ".ico",
            ".icon",
            ".jfif",
            ".tiff",
            ".tif",
            ".gif",
            ".bmp",
            ".odg",
            ".djvu",
            ".odg",
            ".ai",
            ".fla",
            ".pic",
            ".ps",
            ".psb",
            ".svg",
            ".dds",
            ".hdr",
            ".ithmb",
            ".rds",
            ".heic",
            ".aae",
            ".apalbum",
            ".apfolder",
            ".xmp",
            ".dng",
            ".px",
            ".catalog",
            ".ita",
            ".photoscachefile",
            ".visual",
            ".shape",
            ".appicon",
            ".icns",
        },
        "Development": {
            ".py",
            ".h",
            ".m",
            ".jar",
            ".cs",
            ".c",
            ".c#",
            ".cpp",
            ".c++",
            ".class",
            ".java",
            ".php",
            ".phps",
            ".php5",
            ".htm",
            ".html",
            ".css",
            ".xml",
            ".3mf",
            ".o",
            ".obj",
            ".json",
            ".jsonp",
            ".blg",
            ".bbl",
            ".j",
            ".jav",
            ".bash",
            ".bsh",
            ".sh",
            ".rb",
            ".vb",
            ".vbscript",
            ".vbs",
            ".vhd",
            ".vmwarevm",
            ".js",
            ".jsp",
            ".xhtml",
            ".md5",
            ".nib",
            ".strings",
            ".frm",
            ".myd",
            ".myi",
            ".props",
            ".vcxproj",
            ".vs",
            ".lst",
            ".sol",
            ".vbox",
            ".vbox-prev",
            ".pch",
            ".pdb",
            ".lib",
            ".nas",
            ".assets",
            ".sql",
            ".sqlite-wal",
            ".rss",
            ".swift",
            ".xsl",
            ".manifest",
            ".up_meta",
            ".down_meta",
            ".woff",
            ".dist",
            ".sublime-snippet",
            ".d",
            ".ashx",
            ".tpm",
            ".dsw",
            ".hpp",
            ".tga",
            ".kf",
            ".rq",
            ".rdf",
            ".ttl",
            ".pyc",
            ".pyo",
            ".s",
            ".lua",
            ".vim",
            ".p",
            ".dashtoc",
            ".org%2f2000%2fsvg%22%20width%3d%2232%22",
        },
        "Spreadsheet": {
            ".csv",
            ".odf",
            ".ods",
            ".xlr",
            ".xls",
            ".xlsx",
            ".numbers",
            ".xlk",
        },
        "System": {
            ".bif",
            ".shs",
            ".ds_store",
            ".gadget",
            ".so",
            ".idx",
            ".ipmeta",
            ".sys",
            ".dll",
            ".dylib",
            ".etl",
            ".regtrans-ms",
            ".key",
            ".lock",
            ".man",
            ".inf",
            ".x86",
            ".dev",
            ".config",
            ".cfg",
            ".cpl",
            ".cur",
            ".dmp",
            ".drv",
            ".mot",
            ".ko",
            ".supported",
            ".pxe",
            ".cgz",
            ".0",
            ".file",
            ".install",
            ".desktop",
            ".ttc",
            ".ttf",
            ".fnt",
            ".fon",
            ".otf",
            ".download",
            ".acsm",
            ".ini",
            ".opt",
            ".dat",
            ".sav",
            ".save",
            ".aux",
            ".raw",
            ".temp",
            ".tmp",
            ".1",
            ".2",
            ".3",
            ".4",
            ".5",
            ".6",
            ".7",
            ".8",
            ".9",
            ".10",
            ".cache",
            ".ipsw",
            ".stt",
            ".part",
            ".appcache",
            ".sbstore",
            ".gpd",
            ".sqm",
            ".emf",
            ".jrs",
            ".pri",
            ".vcrd",
            ".mui",
            ".localstorage",
            ".localstorage-journal",
            ".data",
            ".crash",
            ".webhistory",
            ".settingcontent-ms",
            ".itc",
            ".atx",
            ".apversion",
            ".apmaster",
            ".apdetected",
            ".pos",
            ".glk",
            ".blob",
            ".cat",
            ".sns",
            ".adv",
            ".asd",
            ".lrprev",
            ".csl",
            ".rdl",
            ".sthlp",
            ".tm2",
            ".mcdb",
            ".fragment",
            ".nif",
            ".blockdata",
            ".continuousdata",
            ".upk",
            ".znb",
            ".xnb",
            ".idrc",
            ".model",
            ".primitives",
            ".ovl",
            ".sid",
            ".stringtable",
            ".foliage",
            ".civ4savedgame",
            ".cgs",
            ".thewitchersave",
            ".pssg",
            ".pac",
            ".unity3d",
            ".ifi",
            ".vmt",
            ".vtf",
            ".pfm",
            ".deu",
            ".map",
            ".simss",
        },
        "Executable": {
            ".exe",
            ".bat",
            ".dmg",
            ".msi",
            ".bin",
            ".pak",
            ".app",
            ".com",
            ".application",
        },
        "Archive": {
            ".zip",
            ".gz",
            ".rar",
            ".cab",
            ".iso",
            ".tar",
            ".lzma",
            ".bz2",
            ".pkg",
            ".xz",
            ".7z",
            ".vdi",
            ".ova",
            ".rpm",
            ".z",
            ".tgz",
            ".deb",
            ".vcd",
            ".ost",
            ".vmdk",
            ".001",
            ".002",
            ".003",
            ".004",
            ".005",
            ".006",
            ".007",
            ".008",
            ".009",
            ".arj",
            ".package",
            ".ims",
        },
        "Backup": {".bak", ".backup", ".back"},
        "Audio": {
            ".mp3",
            ".m3u",
            ".m4a",
            ".wav",
            ".ogg",
            ".flac",
            ".midi",
            ".oct",
            ".aac",
            ".aiff",
            ".aif",
            ".wma",
            ".pcm",
            ".cda",
            ".mid",
            ".mpa",
            ".ens",
            ".adg",
            ".dmpatch",
            ".sngw",
            ".seq",
            ".wem",
            ".mtp",
            ".l6t",
            ".lng",
            ".adx",
            ".link",
        },
        "Database": {
            ".accdb",
            ".accde",
            ".mdb",
            ".mde",
            ".odb",
            ".db",
            ".gdbtable",
            ".gdbtablx",
            ".gdbindexes",
            ".sqlite",
            ".enz",
            ".enl",
            ".sdf",
            ".hdb",
            ".cdb",
            ".gdb",
            ".cif",
            ".xyz",
            ".mat",
            ".bgl",
            ".r",
            ".exp",
            ".asy",
            ".info",
            ".meta",
            ".adf",
            ".appinfo",
            ".xg0",
            ".yg0",
        },
        "Presentation": {".ppt", ".pptx", ".pps", ".ppsx", ".odp", ".key"},
        "Video": {
            ".mpg",
            ".mpeg",
            ".avi",
            ".mp4",
            ".flv",
            ".h264",
            ".mov",
            ".mk4",
            ".swf",
            ".wmv",
            ".mkv",
            ".plist",
            ".m4v",
            ".trec",
            ".3g2",
            ".3gp",
            ".rm",
            ".vob",
        },
        "Bookmark": {".torrent", ".url"},
        "PIM": {
            ".dbx",
            ".eml",
            ".msg",
            ".ics",
            ".pst",
            ".vcf",
            ".gdb",
            ".ofx",
            ".qif",
            ".rem",
            ".tax",
            ".qbmb",
            ".one",
            ".note",
            ".olk14message",
            ".olk14msgattach",
            ".olk14folder",
            ".olkmsgsource",
            ".olk14msgsource",
            ".olk15message",
            ".olk15messageattachment",
            ".olk14event",
            ".olk15msgattachment",
            ".olk15msgsource",
            ".vcs",
            ".hbk",
        },
        "Shortcut": {".lnk"},
    }

    def __init__(self) -> None:
        self.grouped_files: DefaultDict[
            str, DefaultDict[str, Dict[str, Union[int, int]]]
        ] = defaultdict(lambda: defaultdict(lambda: {"count": 0, "size": 0}))
        self.extension_to_category: Dict[str, str] = {
            ext: cat for cat, exts in self.category_mapping.items() for ext in exts
        }
        self.table: Table = Table(title="File Summary")
        self.table.add_column("Category")
        self.table.add_column("File Extension")
        self.table.add_column("Number of Files")
        self.table.add_column("Size")

    def _classify_file(self, filename: Path) -> tuple[str, str, str, int]:
        """
        Classify a file based on its filename and get relevant information.

        Parameters:
        - filename (Path): Path to the file.

        Returns:
        tuple[str, str, str, int]: A tuple containing file information - filename,
        file extension, category, and size.
        """
        filename_str: str = str(filename)
        file_extension: str = Path(filename_str).suffix.lower()
        category: str = self._get_category(file_extension)
        try:
            size: int = stat(filename_str).st_size
        except FileNotFoundError:
            size = 0
        return filename_str, file_extension, category, size

    def add_file(self, filename: Path) -> None:
        """
        Add a file to the categorized files.

        Parameters:
        - filename (Path): Path to the file.
        """
        file_path, file_extension, category, size = self._classify_file(filename)
        self.grouped_files[category][file_extension]["count"] += 1
        self.grouped_files[category][file_extension]["size"] += size

    def update_table(self, size_unit: str = "bytes") -> None:
        """
        Update the summary table with the categorized files.

        Parameters:
        - size_unit (str): Target unit for file sizes (default is "bytes").
        """
        new_table = Table(title="File Summary")
        new_table.add_column("Category")
        new_table.add_column("File Extension")
        new_table.add_column("Number of Files")
        new_table.add_column("Size")

        last_category = None

        for category, extensions in self.grouped_files.items():
            for extension, file_data in extensions.items():
                size = convert_size(file_data["size"], size_unit)

                if last_category is not None and category != last_category:
                    new_table.add_row("", "", "", "")

                new_table.add_row(
                    category if category != last_category else "",
                    extension,
                    str(file_data["count"]),
                    f"{size}",
                )

                last_category = category

        self.table = new_table

    def _get_category(self, file_extension: str) -> str:
        """
        Get the category of a file based on its extension.

        Parameters:
        - file_extension (str): File extension.

        Returns:
        str: File category.
        """
        return self.extension_to_category.get(file_extension, "Other")

    def display_summary(self, size_unit: str = "bytes") -> None:
        """
        Display the categorized file summary using the rich library.

        Parameters:
        - size_unit (str): Target unit for file sizes (default is "bytes").
        """
        console = Console()
        self.update_table(size_unit=size_unit)
        console.print(self.table)

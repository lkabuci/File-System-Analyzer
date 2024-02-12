import os

categories = {
    "image": [".jpg", ".jpeg", ".png", ".gif"],
    "video": [".mp4", ".avi", ".mkv", ".mov"],
    "audio": [".mp3", ".wav", ".flac", ".aiff"],
    "text": [".txt", ".md"],
    "pdf": [".pdf"],
    "archive": [".zip", ".rar", ".7z"],
    "code": [
        ".py",
        ".js",
        ".java",
        ".cpp",
        ".c",
        ".html",
        ".css",
        ".php",
        ".go",
        ".ts",
        ".tsx",
        ".json",
        ".xml",
        ".sh",
    ],
}


def file_categorization(filename: str):
    categoriezed_files = {
        "image": [],
        "video": [],
        "audio": [],
        "text": [],
        "pdf": [],
        "archive": [],
        "code": [],
        "other": [],
    }
    _, extension = os.path.splitext(filename.lower())
    for category, extensions in categories.items():
        if extension in extensions:
            categoriezed_files[category].append(filename)

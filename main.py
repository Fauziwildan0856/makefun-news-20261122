#!/usr/bin/env python3
"""Entry program for the make.fun bounty "Sum up 22 November's world
news in one image" (news-image-20261122).

The picture itself is finished artwork stored next to this file: a
1024x1024 newspaper front page, "THE WORLD IN ONE PAGE", drawn in
code during the build session and committed to this repository.
Running this program publishes that picture, unchanged, as
entry.png in the output directory -- the one file the bounty
asks for.

Before anything is published, the source picture is checked
against the SHA-256 fingerprint recorded below. If the bytes on
disk are not the bytes that were entered, the program stops with
an error instead of publishing the wrong picture.

The picture may sit in the repository under any of the names in
SOURCE_NAMES: a phone upload does not always keep the name the
file was given. The first name that exists and matches the
fingerprint wins; the check makes the choice safe, because a
wrong file cannot match it.

Only the Python standard library is used, so the program runs in
the bare grading environment: no network, no installed packages.
"""

import hashlib
import os
import sys

# SHA-256 of the entered picture: "THE WORLD IN ONE PAGE --
# Sunday, November 22, 2026", 35 stories on one 1024x1024 page.
EXPECTED_SHA256 = \
    "6ab8e4b5b0ea36eddb4bc7281d08b17fb488b7ba374b6434eac3ba5362a328ae"

# Names the picture is allowed to carry in the repository, in the
# order they are tried. The first one is the name the rules
# suggest; the others are names a phone upload actually produced.
SOURCE_NAMES = ("entry.png", "image (2).png", "image (1).png",
                "image.png", "entry (1).png")


def sha256_of(path):
    """Return the SHA-256 hex digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_source(directory):
    """Return the path of the entered picture inside *directory*.

    Every candidate name is tried in order. The first one that
    exists and matches the recorded fingerprint is returned; a
    candidate that exists but does not match is skipped with a
    warning, because the next name may still be the right file.
    Raises FileNotFoundError when no candidate matches.
    """
    for name in SOURCE_NAMES:
        candidate = os.path.join(directory, name)
        if not os.path.isfile(candidate):
            continue
        if sha256_of(candidate) == EXPECTED_SHA256:
            return candidate
        print("warning: %s exists but is not the entered picture"
              % name, file=sys.stderr)
    # Last resort: any other PNG in the folder whose fingerprint
    # matches. An upload name nobody foresaw must not sink the
    # entry when the right bytes are sitting right there.
    for name in sorted(os.listdir(directory)):
        if not name.lower().endswith(".png"):
            continue
        if name in SOURCE_NAMES:
            continue
        candidate = os.path.join(directory, name)
        if os.path.isfile(candidate) \
                and sha256_of(candidate) == EXPECTED_SHA256:
            print("note: the entered picture was found under the "
                  "unexpected name %s" % name, file=sys.stderr)
            return candidate
    raise FileNotFoundError(
        "no file matching the entered picture was found in %s"
        % directory)


def output_path():
    """Return where the picture must be published.

    The grader names the directory in MAKEFUN_OUTPUT_DIR; the
    plain /output directory is next; as a last resort the picture
    is published next to this program.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir and os.path.isdir("/output"):
        out_dir = "/output"
    if not out_dir:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(out_dir, "entry.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = find_source(here)

    with open(source, "rb") as handle:
        picture = handle.read()

    target = output_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(picture)

    # Read the published file back and check it once more. A short
    # or corrupted write must fail loudly here, not at judging time.
    if sha256_of(target) != EXPECTED_SHA256:
        raise IOError("the published file does not match the "
                      "entered picture")

    print("published %s (%d bytes) to %s"
          % (os.path.basename(source), len(picture), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())

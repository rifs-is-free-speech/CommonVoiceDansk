import pandas as pd
import pydub
import os


def clean(file: str, newfile: str=None, convert: bool=False):

    data = pd.read_csv(file, sep="\t", header=0, index_col=0)

    csv = []
    for idx, row in data.iterrows():

        # convert mp3 to wav
        src = f"clips/{row['path']}"
        dst = f"audio/{row['path'].replace('.mp3', '.wav')}"
        if convert:
            convert_mp3_to_wav(src, dst)

            # save text
            with open(f"text/{row['path'].replace('.mp3', '.txt')}", "w") as f:
                f.write(row["sentence"])

        csv.append(
            {
                "id": row["path"].replace(".mp3", ""),
                "text": row["sentence"]
            })

    if not newfile:
        newfile = file.replace(".tsv", ".csv")
    csv = pd.DataFrame(csv)
    csv.to_csv(newfile, index=False)

def convert_mp3_to_wav(
    src: str,
    dst: str,
):
    sound = pydub.AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")


if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    os.makedirs("text", exist_ok=True)

    clean("validated.tsv", "all.csv", False)
    clean("train.tsv")
    clean("dev.tsv")
    clean("test.tsv")
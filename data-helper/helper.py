import json
import os

def process_video_json(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    # Extract transcript segments
    segments = (
        data["actions"][0]["updateEngagementPanelAction"]["content"]
        ["transcriptRenderer"]["content"]["transcriptSearchPanelRenderer"]
        ["body"]["transcriptSegmentListRenderer"]["initialSegments"]
    )

    transcript = " ".join(
        seg["transcriptSegmentRenderer"]["snippet"]["runs"][0]["text"]
        for seg in segments
        if seg.get("transcriptSegmentRenderer", {}).get("snippet", {}).get("runs")
    )

    # Build first ~2 sentences as a description
    sentences = transcript.split(". ")
    description = ". ".join(sentences[:3]).strip()
    if not description.endswith("."):
        description += "."

    output = {
        "id": data["id"],
        "title": data["title"],
        "link": data["link"],
        "description": description,
        "transcript": transcript,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Output written to {output_path}")
    return output


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    input_file = os.path.join(data_dir, "vq9LuCM4YP4.json")
    output_file = os.path.join(data_dir, "vq9LuCM4YP4_output.json")
    process_video_json(input_file, output_file)

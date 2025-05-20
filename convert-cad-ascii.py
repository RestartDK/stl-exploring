import os
from stl import mesh
import stl
import openai

# Load your binary STL file
your_mesh = mesh.Mesh.from_file('USB_Type-C_dust_plug.STL')

# Save as ASCII STL
your_mesh.save('USB_Type-C_dust_plug_ascii.stl', mode=stl.Mode.ASCII)

openai.api_key = os.getenv("API_KEY")

def process_stl_and_ask_shape(file_path, chunk_size=1000, model="gpt-4-turbo"):
    summaries = []
    with open(file_path, 'r') as f:
        chunk = []
        chunk_num = 1
        for i, line in enumerate(f, 1):
            chunk.append(line)
            if i % chunk_size == 0:
                prompt = (
                    f"This is chunk {chunk_num} of an ASCII STL file. "
                    "Please summarize the geometry in this chunk, and list the number of triangles (facets) in this chunk.\n\n"
                    + "".join(chunk)
                )
                print(prompt)
                response = openai.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                print(response.choices[0].message.content)
                summaries.append(response.choices[0].message.content)
                chunk = []
                chunk_num += 1
        if chunk:
            prompt = (
                f"This is chunk {chunk_num} of an ASCII STL file. "
                "Please summarize the geometry in this chunk, and list the number of triangles (facets) in this chunk.\n\n"
                + "".join(chunk)
            )
            print(prompt)
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            print(response.choices[0].message.content)
            summaries.append(response.choices[0].message.content)

    # Aggregate summaries and ask the high-level question
    aggregate_prompt = (
        "Here are summaries of chunks from an ASCII STL file:\n\n"
        + "\n\n".join(summaries)
        + "\n\nBased on these summaries, what shape is this object? Please provide your reasoning."
    )
    final_response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": aggregate_prompt}],
        max_tokens=500
    )
    print("Final shape analysis:\n", final_response.choices[0].message.content)

# Usage
process_stl_and_ask_shape("USB_Type-C_dust_plug_ascii.stl", chunk_size=1000)
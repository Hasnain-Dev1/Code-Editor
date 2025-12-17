import streamlit as st
import tempfile
import subprocess
from pathlib import Path

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Code Editor", layout="wide")
st.title("⚡ Advanced Code Editor & Runner")

st.markdown("""
**⚠️ Warning:**  
This app executes arbitrary code on the machine where it runs.  
Use only in a **safe/trusted environment** (or inside a container).  
Runtime limits are *not enforced strictly*.  
""")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.header("⚙️ Runner Settings")
    language = st.selectbox(
        "Language", ["python", "bash", "javascript (node)", "c", "cpp", "java"], index=0
    )
    timeout = st.slider("Timeout (seconds)", 1, 60, 10)
    show_stderr = st.checkbox("Show stderr (errors)", value=True)
    use_ace = st.checkbox("Use advanced editor (streamlit-ace)", value=True)
    samples_expand = st.expander("📚 Load sample code")

# ------------------ Sample Programs ------------------
samples = {
    "python": "print('Hello from Python')\nname = input('Your name: ')\nprint('Hello,', name)",
    "bash": "#!/usr/bin/env bash\necho Hello from bash\nread -p 'Your name: ' name\necho Hello, $name",
    "javascript (node)": """console.log('Hello from Node');
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
rl.question('Your name: ', (name) => { console.log(`Hello, ${name}`); rl.close(); });""",
    "c": """#include <stdio.h>
int main(){ char name[100]; printf("Your name: "); scanf("%99s", name); printf("Hello, %s\\n", name); return 0; }""",
    "cpp": """#include <iostream>
using namespace std;
int main(){ string name; cout<<"Your name: "; cin>>name; cout<<"Hello, "<<name<<"\\n"; return 0; }""",
    "java": """import java.util.*;
public class Main {
  public static void main(String[] args){
    Scanner s = new Scanner(System.in);
    System.out.print("Your name: ");
    String name = s.next();
    System.out.println("Hello, " + name);
  }
}""",
}

with samples_expand:
    for k in samples:
        if st.button(f"Load sample: {k}"):
            st.session_state["code"] = samples[k]
            st.session_state["lang"] = k

# ------------------ Session State Defaults ------------------
if "code" not in st.session_state:
    st.session_state["code"] = samples["python"]
if "lang" not in st.session_state:
    st.session_state["lang"] = "python"

# Keep sidebar language synced
if language != st.session_state.get("lang", ""):
    st.session_state["lang"] = language

# ------------------ Layout ------------------
editor_cols = st.columns([3, 1])

# ------------------ Code Editor ------------------
with editor_cols[0]:
    st.subheader("✍️ Code Editor")
    if use_ace:
        try:
            from streamlit_ace import st_ace

            code = st_ace(
                value=st.session_state["code"],
                language=st.session_state["lang"],
                theme="monokai",
                key="ace",
                height=360,
            )
        except Exception:
            st.warning("⚠️ streamlit-ace not available - using textarea")
            code = st.text_area("Code", st.session_state["code"], height=360)
    else:
        code = st.text_area("Code", st.session_state["code"], height=360)

    st.session_state["code"] = code

# ------------------ Files and Actions ------------------
with editor_cols[1]:
    st.subheader("📂 Files & Actions")

    # Upload code
    uploaded = st.file_uploader("Upload Code File")
    if uploaded:
        st.session_state["code"] = uploaded.read().decode("utf-8")
        st.success("✅ File loaded into editor!")

    # Download code
    st.download_button(
        "💾 Download Code",
        st.session_state["code"],
        file_name=f"code.{language.split()[0]}",
    )

    # Run Button
    if st.button("▶️ Run Code"):
        with tempfile.TemporaryDirectory() as tmpdir:
            ext_map = {
                "python": "py",
                "bash": "sh",
                "javascript (node)": "js",
                "c": "c",
                "cpp": "cpp",
                "java": "java",
            }
            ext = ext_map[language]
            code_file = Path(tmpdir) / f"main.{ext}"
            code_file.write_text(st.session_state["code"])

            commands = {
                "python": f"python {code_file}",
                "bash": f"bash {code_file}",
                "javascript (node)": f"node {code_file}",
                "c": f"gcc {code_file} -o {tmpdir}/a.out && {tmpdir}/a.out",
                "cpp": f"g++ {code_file} -o {tmpdir}/a.out && {tmpdir}/a.out",
                "java": f"javac {code_file} && java -cp {tmpdir} Main",
            }

            cmd = commands[language]

            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=tmpdir,
                )
                st.success("✅ Execution finished")
                st.code(result.stdout if result.stdout else " ", language="text")
                if show_stderr and result.stderr:
                    st.error(result.stderr)
            except subprocess.TimeoutExpired:
                st.error("⏱ Timeout reached!")

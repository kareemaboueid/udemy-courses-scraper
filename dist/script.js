function copy_text(p_element) {
    const text = p_element.textContent;

    navigator.clipboard.writeText(text).then(() => {
        p_element.classList.remove("txt");
        p_element.classList.add("txt-copied");
    });
}

function save_to_file() {
    const course_name = document.querySelector(
        ".info_details p strong + a"
    ).textContent;
    const output_path = `./${course_name}_sections.txt`;
    const sections = document.querySelectorAll(".single_data_section");

    let text_content = "";

    sections.forEach(section => {
        const title = section.querySelector(".title p").textContent.trim();
        const duration = section
            .querySelector(".duration p")
            .textContent.trim();
        text_content += `${title}\n${duration} minutes\n\n`;
    });

    const blob = new Blob([text_content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = output_path;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

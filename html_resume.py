import yaml
from pathlib import Path
from src.resume_schemas.resume import Resume  # Import your Resume model
from src.libs.resume_and_cover_builder.resume_generator import ResumeGenerator

# Load resume.yaml
def load_resume_from_yaml(yaml_path: str) -> Resume:
    resume = None
    with open(yaml_path, 'r', encoding='utf-8') as file:
        resume = Resume(file)
    return resume

# Initialize
def main():
    yaml_resume_path = "data_folder/plain_text_resume.yaml"  # <-- Path to your resume YAML
    style_css_path = "src/libs/resume_and_cover_builder/resume_style/style_josylad_blue.css"      # <-- Path to your CSS template
    output_html_path = "data_folder/output/resume.html" # <-- Where you want to save the HTML

    # Load resume from YAML
    resume_object = load_resume_from_yaml(yaml_resume_path)

    # Check if open_ai_calls.json exists to decide offline or online mode
    saved_openai_responses = Path("data_folder/output/open_ai_calls.json")
    offline_mode = saved_openai_responses.exists()

    # Initialize ResumeGenerator based on mode
    resume_generator = ResumeGenerator(
        offline_mode=offline_mode,
        saved_responses_path=saved_openai_responses if offline_mode else None
    )

    # Set resume object
    resume_generator.set_resume_object(resume_object)

    # Generate HTML resume
    html_resume = resume_generator.create_resume(style_css_path)

    # Save to output
    Path(output_html_path).parent.mkdir(parents=True, exist_ok=True)  # Ensure output folder exists
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_resume)

    print(f"Resume generated successfully at {output_html_path}")

if __name__ == "__main__":
    main()

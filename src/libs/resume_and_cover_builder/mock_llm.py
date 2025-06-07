import json
from pathlib import Path
import re

class MockLLMResumer:
    def __init__(self, saved_responses_path, strings=None):
        self.saved_responses_path = saved_responses_path
        self.sections = {}
        self.strings = strings  # not really needed here, but kept for compatibility

    def set_resume(self, resume):
        self.resume = resume
        self._load_saved_sections()

    def _load_saved_sections(self):
        with open(self.saved_responses_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            logs = json.loads(content) 

        for log in logs:
            reply = log.get("replies", "")
            section_id = self._extract_section_id(reply)
            if "<header>" in reply:
                self.sections['header'] = reply
            elif section_id == "education":
                self.sections['education'] = reply
            elif section_id == "work-experience":
                self.sections['work_experience'] = reply
            elif section_id == "side-projects":
                self.sections['projects'] = reply
            elif section_id == "achievements":
                self.sections['achievements'] = reply
            elif section_id == "certifications":
                self.sections['certifications'] = reply
            elif section_id == "skills-languages":
                self.sections['additional_skills'] = reply

    @staticmethod
    def _extract_section_id(html_content):
        """
        Extracts the section id from HTML content.
        """
        match = re.search(r'<section\s+id="([^"]+)"', html_content)
        if match:
            return match.group(1)
        return None

    def generate_html_resume(self) -> str:
        body_html = f"  {self.sections.get('header', '')}\n"
        body_html += "  <main>\n"
        body_html += f"    {self.sections.get('education', '')}\n"
        body_html += f"    {self.sections.get('work_experience', '')}\n"
        body_html += f"    {self.sections.get('projects', '')}\n"
        body_html += f"    {self.sections.get('achievements', '')}\n"
        body_html += f"    {self.sections.get('certifications', '')}\n"
        body_html += f"    {self.sections.get('additional_skills', '')}\n"
        body_html += "  </main>\n"
        return body_html

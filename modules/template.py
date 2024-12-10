from modules import BaseModule
import logging
import jinja2

logger = logging.getLogger(__name__)

class TemplateModule(BaseModule):
    def process(self, ssh_client):
        src = self.params.get("src")
        dest = self.params.get("dest")
        vars = self.params.get("vars", {})

        if not src or not dest:
            logger.error("Missing 'src' or 'dest' in parameters")
            return

        try:
            with open(src, 'r') as template_file:
                template_content = template_file.read()

            template = jinja2.Template(template_content)
            rendered_content = template.render(vars)

            sftp = ssh_client.open_sftp()
            with sftp.file(dest, "w") as remote_file:
                remote_file.write(rendered_content)
                logger.info(f"Templated {src} to {dest}")
            sftp.close()
        except Exception as e:
            logger.error(f"Failed to template {src} to {dest}: {e}")

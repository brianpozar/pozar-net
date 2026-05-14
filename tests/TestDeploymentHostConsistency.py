import re
import unittest
from pathlib import Path
from urllib.parse import urlparse


class TestDeploymentHostConsistency(unittest.TestCase):
    def testWorkflowBaseUrlHostMatchesCnameHost(self) -> None:
        workflowContent = Path(".github/workflows/hugo.yml").read_text(encoding="utf-8")
        baseUrlMatch = re.search(r"hugo\s+--minify\s+--baseURL\s+(\S+)", workflowContent)

        self.assertIsNotNone(
            baseUrlMatch,
            "Expected Hugo deploy workflow to define --baseURL in .github/workflows/hugo.yml",
        )

        baseUrl = baseUrlMatch.group(1).strip("'\"")
        baseUrlHost = urlparse(baseUrl).hostname
        cnameHost = Path("static/CNAME").read_text(encoding="utf-8").strip().rstrip("/")

        self.assertEqual(
            baseUrlHost,
            cnameHost,
            (
                "Deploy baseURL host must match static/CNAME host so CSS/JS asset URLs stay same-origin "
                "and are not blocked by Subresource Integrity checks."
            ),
        )


if __name__ == "__main__":
    unittest.main()

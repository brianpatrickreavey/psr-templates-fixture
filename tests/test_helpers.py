"""
Test helpers for PSR template integration tests.
Parses and validates rendered templates (addon.xml, CHANGELOG.md).
Supports semantic validation of release structure and content.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class ReleaseInfo:
    """Parsed release information from changelog."""
    version: str
    date: Optional[str] = None
    sections: Optional[Dict[str, List[str]]] = None  # section_name -> list of items
    raw_content: str = ""
    
    def __post_init__(self):
        if self.sections is None:
            self.sections = {}


@dataclass
class AddonXmlInfo:
    """Parsed addon.xml information."""
    id: str
    version: str
    name: Optional[str] = None
    provider_name: Optional[str] = None
    news_url: Optional[str] = None
    news_content: Optional[str] = None
    raw_xml: str = ""


class AddonXmlParser:
    """Parser for Kodi addon.xml files with template rendering validation."""
    
    @staticmethod
    def parse(addon_xml_path: Path) -> AddonXmlInfo:
        """
        Parse addon.xml and extract key information.
        
        Args:
            addon_xml_path: Path to addon.xml file
            
        Returns:
            AddonXmlInfo with parsed data
            
        Raises:
            FileNotFoundError: If addon.xml not found
            xml.etree.ElementTree.ParseError: If XML is malformed
        """
        if not addon_xml_path.exists():
            raise FileNotFoundError(f"addon.xml not found at {addon_xml_path}")
        
        raw_xml = addon_xml_path.read_text()
        tree = ET.parse(addon_xml_path)
        root = tree.getroot()
        
        # Extract root attributes
        addon_id = root.get("id", "")
        version = root.get("version", "")
        name_elem = root.find("name")
        name = name_elem.text if name_elem is not None else ""
        
        # Extract provider name from info element
        provider_name = None
        for info in root.findall("extension"):
            if info.get("point") == "xbmc.addon.metadata":
                prov = info.find("provider")
                if prov is not None:
                    provider_name = prov.text
                break
        
        # Extract news URL if present in metadata
        news_url = None
        news_content = None
        for extension in root.findall("extension"):
            if extension.get("point") == "xbmc.addon.metadata":
                # Look for news element or news URL
                news_elem = extension.find("news")
                if news_elem is not None:
                    news_content = news_elem.text
                news_url_elem = extension.find("news_url")
                if news_url_elem is not None:
                    news_url = news_url_elem.text
                break
        
        return AddonXmlInfo(
            id=addon_id,
            version=version,
            name=name if name else None,
            provider_name=provider_name,
            news_url=news_url,
            news_content=news_content,
            raw_xml=raw_xml
        )
    
    @staticmethod
    def validate_version(addon_info: AddonXmlInfo, expected_version: str) -> bool:
        """
        Validate addon version matches expected version.
        
        Args:
            addon_info: Parsed addon info
            expected_version: Expected version string
            
        Returns:
            True if versions match (with or without 'v' prefix)
        """
        actual_version = addon_info.version
        expected_clean = expected_version.lstrip('v')
        return actual_version == expected_clean
    
    @staticmethod
    def extract_news_section(addon_info: AddonXmlInfo) -> Optional[str]:
        """
        Extract rendered news section from addon.xml.
        
        Returns news content if present, None otherwise.
        """
        return addon_info.news_content


class ChangelogParser:
    """Parser for CHANGELOG.md files with template validation."""
    
    # Regex patterns for changelog parsing
    RELEASE_HEADER = re.compile(r'^## v?(\d+\.\d+\.\d+)(?:\s+\((.+?)\))?$', re.MULTILINE)
    SECTION_HEADER = re.compile(r'^### ([A-Za-z\s]+)$', re.MULTILINE)
    LIST_ITEM = re.compile(r'^[-*+]\s+(.+)$', re.MULTILINE)
    
    @staticmethod
    def parse(changelog_path: Path) -> List[ReleaseInfo]:
        """
        Parse CHANGELOG.md and extract release information.
        
        Args:
            changelog_path: Path to CHANGELOG.md file
            
        Returns:
            List of ReleaseInfo objects in order of appearance
            
        Raises:
            FileNotFoundError: If CHANGELOG.md not found
        """
        if not changelog_path.exists():
            raise FileNotFoundError(f"CHANGELOG.md not found at {changelog_path}")
        
        content = changelog_path.read_text()
        releases = []
        
        # Split by release headers
        release_matches = list(ChangelogParser.RELEASE_HEADER.finditer(content))
        
        for i, match in enumerate(release_matches):
            version = match.group(1)
            date = match.group(2)
            
            # Get content between this release and the next
            start_pos = match.end()
            end_pos = release_matches[i + 1].start() if i + 1 < len(release_matches) else len(content)
            release_content = content[start_pos:end_pos].strip()
            
            # Parse sections within this release
            sections = ChangelogParser._parse_sections(release_content)
            
            releases.append(ReleaseInfo(
                version=version,
                date=date,
                sections=sections,
                raw_content=release_content
            ))
        
        return releases
    
    @staticmethod
    def _parse_sections(content: str) -> Dict[str, List[str]]:
        """
        Parse section headers and items within release content.
        
        Args:
            content: Content block for a single release
            
        Returns:
            Dict of section_name -> list of items
        """
        sections: Dict[str, List[str]] = {}
        current_section = "General"
        sections[current_section] = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            section_match = ChangelogParser.SECTION_HEADER.match(line)
            if section_match:
                current_section = section_match.group(1).strip()
                sections[current_section] = []
                continue
            
            item_match = ChangelogParser.LIST_ITEM.match(line)
            if item_match:
                item_text = item_match.group(1).strip()
                if current_section in sections:
                    sections[current_section].append(item_text)
        
        # Remove empty sections
        return {k: v for k, v in sections.items() if v}
    
    @staticmethod
    def get_release(releases: List[ReleaseInfo], version: str) -> Optional[ReleaseInfo]:
        """
        Get a specific release by version number.
        
        Args:
            releases: List of parsed releases
            version: Version to find (e.g., "0.1.0")
            
        Returns:
            ReleaseInfo if found, None otherwise
        """
        clean_version = version.lstrip('v')
        for release in releases:
            if release.version == clean_version:
                return release
        return None
    
    @staticmethod
    def validate_release_exists(releases: List[ReleaseInfo], version: str) -> bool:
        """Check if a specific version exists in releases."""
        return ChangelogParser.get_release(releases, version) is not None
    
    @staticmethod
    def validate_all_versions_present(releases: List[ReleaseInfo], expected_versions: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that all expected versions are present in changelog.
        
        Args:
            releases: List of parsed releases
            expected_versions: List of expected version strings
            
        Returns:
            Tuple of (all_present: bool, missing_versions: List[str])
        """
        missing = []
        for version in expected_versions:
            if not ChangelogParser.validate_release_exists(releases, version):
                missing.append(version)
        return len(missing) == 0, missing
    
    @staticmethod
    def get_all_versions(releases: List[ReleaseInfo]) -> List[str]:
        """Get list of all versions in changelog (in order)."""
        return [r.version for r in releases]


class JinjaTemplateValidator:
    """Validator for Jinja2 rendered content."""
    
    @staticmethod
    def validate_no_undefined_vars(content: str) -> Tuple[bool, List[str]]:
        """
        Check rendered content for common Jinja2 undefined patterns.
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []
        
        # Check for common undefined patterns
        undefined_patterns = [
            (r'\{\{\s*\w+\s*\}\}', "Unrendered variable"),
            (r'\{%\s*\w+.*?%\}', "Unrendered control block"),
            (r'undefined', "Undefined reference"),
            (r'None', "Null/None value in output"),
        ]
        
        # Only flag these if they appear in suspicious contexts
        # (e.g., not in comments or code blocks)
        if "{{" in content or "{%" in content:
            errors.append("Potential unrendered Jinja2 syntax found")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_xml_structure(raw_xml: str) -> Tuple[bool, List[str]]:
        """
        Validate XML structure is well-formed.
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []
        try:
            ET.fromstring(raw_xml)
        except ET.ParseError as e:
            errors.append(f"XML Parse Error: {str(e)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_markdown_format(content: str) -> Tuple[bool, List[str]]:
        """
        Validate Markdown format (basic checks).
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []
        
        # Check for unmatched brackets
        open_count = content.count('[')
        close_count = content.count(']')
        if open_count != close_count:
            errors.append(f"Unmatched brackets: {open_count} open, {close_count} close")
        
        # Check for incomplete links
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]*)\)')
        incomplete_links = re.findall(r'\[([^\]]+)\](?!\()', content)
        if incomplete_links:
            errors.append(f"Incomplete markdown links: {incomplete_links}")
        
        return len(errors) == 0, errors

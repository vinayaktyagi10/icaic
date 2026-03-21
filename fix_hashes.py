import base64
import re
import urllib.parse

def fix_action_hashes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_hash(match):
        full_attr = match.group(0)
        attr_name = match.group(1)
        attr_value = match.group(2)
        
        # attr_value is something like #elementor-action%3Aaction%3Dlightbox%26settings%3D...
        if 'settings%3D' in attr_value:
            parts = attr_value.split('settings%3D')
            if len(parts) == 2:
                prefix = parts[0] + 'settings%3D'
                encoded_settings = parts[1]
                
                # The encoded_settings might be followed by other things or end with " or '
                # But here it's at the end of the attribute value
                try:
                    # URL decode
                    decoded_url = urllib.parse.unquote(encoded_settings)
                    # Base64 decode
                    decoded_b64 = base64.b64decode(decoded_url).decode('utf-8')
                    
                    # Replace absolute URL with relative
                    # Since it's index.html, rel_prefix is empty
                    new_decoded = decoded_b64.replace('https:\\/\\/icaic.in\\/wp-content\\/', 'wp-content\\/')
                    new_decoded = new_decoded.replace('https:\\/\\/icaic.in\\/wp-includes\\/', 'wp-includes\\/')
                    
                    # Re-encode
                    new_b64 = base64.b64encode(new_decoded.encode('utf-8')).decode('utf-8')
                    # Re-URL encode
                    new_encoded_url = urllib.parse.quote(new_b64)
                    
                    return f'{attr_name}="{prefix}{new_encoded_url}"'
                except Exception as e:
                    print(f"Error processing hash: {e}")
                    return full_attr
        return full_attr

    # Regex to find data-e-action-hash="..." or '...'
    pattern = r'(data-e-action-hash)=["\']([^"\']+)["\']'
    new_content = re.sub(pattern, replace_hash, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed action hashes in {file_path}")

if __name__ == "__main__":
    fix_action_hashes('index.html')

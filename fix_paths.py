import os

def fix_html_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                depth = root.count(os.sep)
                if root == '.':
                    depth = 0
                else:
                    # If we are in ./subdir, depth should be 1
                    # os.walk('.') prefix means root starts with '.'
                    depth = root.count(os.sep) 
                
                # Correction for depth
                # '.' -> 0
                # './subdir' -> 1
                # './subdir/sub' -> 2
                
                rel_prefix = "../" * depth
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                new_content = content
                
                # literal
                new_content = new_content.replace('https://icaic.in/wp-content/', rel_prefix + 'wp-content/')
                new_content = new_content.replace('https://icaic.in/wp-includes/', rel_prefix + 'wp-includes/')
                
                # escaped
                new_content = new_content.replace('https:\\/\\/icaic.in\\/wp-content\\/', rel_prefix.replace('/', '\\/') + 'wp-content\\/')
                new_content = new_content.replace('https:\\/\\/icaic.in\\/wp-includes\\/', rel_prefix.replace('/', '\\/') + 'wp-includes\\/')
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_html_files()

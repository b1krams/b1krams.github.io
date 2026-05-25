import os
from bs4 import BeautifulSoup

directory = r'e:\code\b1krams.github.io'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html') and not file.startswith('old_'):
            if root == directory and file == 'index.html':
                continue
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Check if already processed
                nav = soup.find('nav', class_='global-nav')
                if not nav:
                    continue
                
                brand = nav.find('a', class_='global-nav-brand')
                if not brand:
                    continue
                    
                # If brand's parent is already our flex wrapper, it might be already processed
                if brand.parent.name == 'div' and 'flex' in brand.parent.get('class', []):
                    # check if we already moved it
                    if brand.parent.find('h1'):
                        print(f"Skipping {filepath} - already processed")
                        continue

                h1 = soup.body.find('h1')
                if not h1:
                    print(f"No H1 found in {filepath}")
                    continue

                # Save h1 content and style
                h1_content = "".join(str(c) for c in h1.contents)
                h1_style = h1.get('style', '')

                # Find the immediate wrapper of h1 (usually a div that holds h1 and p)
                parent = h1.parent
                
                # Remove h1
                h1.extract()
                
                # Remove subtitle p if it exists right after or is in the same parent
                p = parent.find('p')
                if p:
                    p.extract()

                # If parent has no significant text left, remove the parent
                text_left = parent.get_text(strip=True)
                if not text_left and not parent.find_all():
                    parent.extract()
                
                # Modify nav
                # Create wrapper
                wrapper = soup.new_tag('div', attrs={'class': 'flex items-center'})
                brand.wrap(wrapper)
                
                # Create new h1 container
                title_container = soup.new_tag('div', attrs={'class': 'hidden sm:block border-l border-slate-700/60 pl-4 ml-4 py-1'})
                new_h1 = soup.new_tag('h1', attrs={'class': 'text-sm font-bold text-slate-200 m-0 leading-none'})
                if h1_style:
                    new_h1['style'] = h1_style
                    
                new_h1.append(BeautifulSoup(h1_content, 'html.parser'))
                title_container.append(new_h1)
                
                wrapper.append(title_container)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"Successfully processed {filepath}")
            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

print("Done.")

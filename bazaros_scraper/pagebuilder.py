def generate_div_string_from_dict(dict:dict) -> str:
    output = "\t<div class='box'>\n"
    output += f"\t\t<h1>{dict['title']}</h1>\n"
    output += f"\t\t<img src = {dict['img-url']} alt='image'>\n"
    output += f"\t\t<p>Price: {dict['price']} {dict['currency']}</p>\n"
    output += "\t</div>\n"
    return output

def generate_html_from_template(template_path, destination_path, div_list):
    template = ""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.readlines()# ["", "",""]
        template = "".join(template)
    for div in div_list:
        template += div
    template += "</body>"
    template += "</html>"
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(template)
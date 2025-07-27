class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value
        
        if self.tag in ["img", "br", "hr"]:
            if self.tag == "img":
                return f'<{self.tag} src="{self.props["src"]}" alt="{self.props["alt"]}">'
            else:
                return f'<{self.tag}>'
        
        else:
            html_content = ""
            if self.children:  # Make sure children exist
                for child in self.children:
                    html_content += child.to_html()  # Add each child's HTML to the string
            return f"<{self.tag}>{html_content}</{self.tag}>"
    
    def props_to_html(self):
        strings = []

        if not self.props:
            return None

        for prop in self.props:
            strings.append(f'{prop}="{self.props[prop]}"')
        return " ".join(strings)
    
    def __repr__(self):
        return f"tag={self.tag}, value={self.value}, children={self.children}, props = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            if self.props_to_html() == None:
                return f'<{self.tag}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
            
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("Ain't got no kids")
        
        childs = []
        for child in self.children:
            childs.append(child.to_html())
        html_children = "".join(childs)
            
        if self.props_to_html() == None:
            return f'<{self.tag}>{html_children}</{self.tag}>'
        else:
            return f'<{self.tag} {self.props_to_html()}>{html_children}</{self.tag}>'
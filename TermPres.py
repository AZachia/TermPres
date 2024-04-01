import color
from color import terminal_size
import json
from PIL import Image
from art import text2art


def fill_terminal(text:str = " "):
    ts = terminal_size()
    for _ in range(ts[1] - 1):
        print(text*ts[0])
        

def to_roman(n):
    result = ""
    for numeral, value in (("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
                           ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
                           ("X", 10), ("IX", 9), ("V", 5), ("IV", 4),
                           ("I", 1)):
        result += numeral*(n//value)
        n %= value
    return result




class Slide:
    def __init__(self, title = "New Slide", bg = "#FFFFFF", fg = "#000000"):
        self.content = {"title": title, "bg": bg, "fg": fg, "text": []}
        
    
    def set_bg(self, color):
        self.content["bg"] = color
        
    def copy(self):
        temp = Slide()
        temp.content = self.content.copy()
        
        return temp
    
    def add_text(self, text, fg = None, bg = None, align = "left", x = 3, y = None, type:str ="text"):
        self.content["text"].append({"text": text, "fg": fg, "bg": bg, "align": align, "x": x, "y": y, 'type': type})
        
    def add_enum(self, enum : list = [], fg = None, bg = None, align = "left", x = None, y = None, bullet = "•"):
        text = ""
        for i, item in enumerate(enum):
            blt = bullet.replace("{i}", str(i+1))
            blt = blt.replace("{I}", to_roman(i+1))
            text += f"{blt} {item}\n"
        self.add_text(text, fg, bg, align, x, y, type="enum")
        
    def add_image(self, img: str | Image.Image, h: int =20, w:int = 20, *args, **kwargs):
        if isinstance(img, str):
            img = Image.open(img)
        img = img.resize((w, h))
        
        pix = []
        for y in range(h):
            ligne_couleurs = []
            for x in range(w):
                couleur = img.getpixel((x, y))[0:3]
                ligne_couleurs.append(color.get_hex_print(color.color(couleur).hex(), True) + " ")
            pix.append(ligne_couleurs)
        
        image = "\n".join(["".join(ligne) for ligne in pix])
        self.add_text(image, *args, **kwargs, type="img")
        

        
    
    
    

class TermPresentation:
    def __init__(self):
        self.content = {"slides": []}
        self.current_slide = 0
    
    def add_slide(self, slide: Slide):
        self.content["slides"].append(slide.content)
    
    def remove_slide(self, index):
        self.content["slides"].pop(index)
    
    def insert_slide(self, index, slide: Slide):
        self.content["slides"].insert(index, slide.content)
        
    
    def next_slide(self):
        self.current_slide += 1
        self.show()
    
    
    def show(self, slide_index = 0, end_index = 1):
        
        temp = Slide(bg="#000000", fg="#FFFFFF")
        temp.add_text("Presentation Ended, press 'Enter' to quit", align="center", y=5)
        if not temp in self.content["slides"]:
            self.add_slide(temp)
        
        
        print(end=color.hide_cursor)
        
        for slide in self.content["slides"][slide_index:-end_index]:
    
            
            reset = color.get_hex_print(color.color(slide["bg"]).hex(), True) + color.get_hex_print(color.color(slide["fg"]).hex())
            
            
            print(reset)
            color.clear()
            fill_terminal()
            
            print(color.cursor_pos2(0, 0), end="")
            
            for text in slide["text"]:
                fg = text["fg"] or slide["fg"]
                bg = text["bg"] or slide["bg"]
                align = text["align"]
                x = text["x"] or 0
                y = text["y"] or 0
                
                print(end="\n"*abs(y))
                
                color_string = color.get_hex_print(color.color(fg).hex()) + color.get_hex_print(color.color(bg).hex(), True)
                
                
                for line in text["text"].split("\n"):
                
                    if align == "left":
                        
                        formated = color_string + line
                        formated = " "*abs(x) + formated
                        
                        
                    elif align == "center":
                        formated = color_string + line

                        formated = color.center(formated)
                        formated = " "*abs(x) + formated
                    
                    elif align == "right":
                        
                        formated = color_string + line
                        formated = " "*((terminal_size()[0] - len(color.colorless(formated))) - x) + formated
                    
                    print(formated + reset)

            
            inpt = input()
            # if input == '':
            #     self.next_slide()
        print(color.reset+color.show_cursor)
        color.clear()
        
    def save(self, path):
        with open(path, "w") as file:
            json.dump(self.content, file, indent=4)
    
    def load(self, path):
        with open(path, "r") as file:
            self.content = json.load(file)
        
            
        
        
        
       
        
    


if __name__ == "__main__":
    

    
    
    pres = TermPresentation()
    
    p1 = Slide()
    p1.add_text(f"{color.bold}{text2art('TermPres', 'tarty1')}{color.reset}", fg = "#FF0000", align = "center", y = 0)
    p1.add_text(f"{color.bold} The TermPresentation Library{color.reset}", fg = "#FF0000", align = "center", y = 2)
    p1.add_text(" A simple library for creating \nterminal presentations", align = "center")
    p1.add_text("Table of Contents", fg = "#0000FF", x=2)
    p1.add_enum(["Introduction", "Installation", "Usage"], align = "left", x=5, bullet = "{I}.", y=1)
    p1.add_text('', y=2)
    p1.add_image("term.png", h=20, w=50, align="left", x=5)
    
    pres.add_slide(p1)
    
    p2 = Slide()
    p2.add_text(text2art("Introduction"), align = "left", y=2)
    p2.add_text("TermPresentation is a simple library for creating terminal presentations")
    p2.add_text("It is designed to be simple and easy to use")
    
    p2.add_text("Features", y=2)
    p2.add_enum(["Simple to use", "Customizable", "Supports images", "Easy way to import and export", "Multiple font support", "color support"], x = 5, y=2)
    
    p2.add_image("pres.png", h=30, w=95, align="left", x=5)
    
    pres.add_slide(p2)
    
    p3 = Slide(bg="#EFEFEF")
    p3.add_text(text2art("Installation"), y=2)
    p3.add_text("You can install TermPresentation by coping the file in your directory")
    p3.add_image("dw.png", h=25, w=50, align="center")

    
    pres.add_slide(p3)
    
    p4 = Slide()
    p4.add_text(text2art("Usage"))
    p4.add_text("To use TermPresentation, you must first import it:")
    p4.add_text(f"{color.green}from{color.blue} TermPresentation {color.green}import{color.blue} TermPresentation, Slide{color.reset}")
    
    p4.add_text("Then you can create a presentation:", y=2)
    p4.add_text(f"{color.green}pres{color.blue} = TermPresentation()")
    p4.add_text(f"{color.green}slide{color.blue} = Slide()")
    p4.add_text(f"{color.green}slide{color.blue}.add_text('Hello World!')")
    p4.add_text(f"{color.green}pres{color.blue}.add_slide(slide)")
    
    p4.add_text("You can also add images:", y=2)
    p4.add_text(f"{color.green}slide{color.blue}.add_image('mario.png', h=30, w=50, align='left', x=5)")
    
    p4.add_text("Finally, you can show the presentation:", y=2)
    p4.add_text(f"{color.green}pres{color.blue}.show()")
    
    p4.add_image("mario.png", h=30, w=50, align="left", x=5)

    
    pres.add_slide(p4)
    
    pres.show()
    
    
    pres.save("intro.tp")
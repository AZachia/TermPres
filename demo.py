from TermPres import TermPresentation, Slide


pres = TermPresentation()


slide = Slide("Title")
slide.add_text("This is a slide")
slide.add_enum(["you can add", "a list", "of items"])
slide.add_text("And even images:")
slide.add_image("mario.png", h=30, w=50, align="left", x=5)


pres.add_slide(slide)

pres.show()

pres2 = TermPresentation()
pres2.load("intro.tp")
pres2.show()

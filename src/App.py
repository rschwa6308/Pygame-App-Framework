from Hoster import *
from GridView import *

class App:
    def __init__(self, hoster: Hoster):
        self.hoster = hoster
        self.hoster.trigger_update = self.update_screen
        self.alive = False
    
    def update_screen(self):
        self.hoster.render_onto(self.screen)
        pygame.display.update()
    
    def run(self, screen_dims=(800, 600)):
        self.alive = True
        self.screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)

        while self.alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_screen()


if __name__ == "__main__":
    test_component = GridView(layout=[
        [View(5, 1, RED), View(1, 1, GREEN)],
        [View(6, 1, BLUE)]
    ])

    test_hoster = Hoster(
        {"test_page": test_component},
        "test_page"
    )

    test_app = App(test_hoster)
    test_app.run()

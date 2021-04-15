from django.db import models


class Player(models.Model):
    discord_id = models.CharField(max_length=255, blank=False, primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    signup = models.BooleanField(blank=False)

    def __str__(self):
        return self.name


class Deck(models.Model):
    name = models.CharField(max_length=255, blank=False)
    side = models.CharField(max_length=255, blank=False, choices=(('corp', 'Corp'), ('runner', 'Runner')))
    url = models.CharField(max_length=255, blank=False)
    image_url = models.CharField(max_length=255, blank=False)
    faction = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name
    
    def color(self):
        if self.faction == 'shaper':
            return 'color: #065f46'
        if self.faction == 'criminal':
            return 'color: #1e40af'
        if self.faction == 'anarch':
            return 'color: #92400e'
        if self.faction == 'jinteki':
            return 'color: #991b1b'
        if self.faction == 'hb':
            return 'color: #3730a3'
        if self.faction == 'nbn':
            return 'color: #d97706'
        if self.faction == 'weyland':
            return 'color: #064e3b'
        return ''

    def img(self):
        return '/static/' + self.image_url


class Week(models.Model):
    start = models.DateField(blank=False)

    def __str__(self):
        return self.start.strftime('%B %-e %Y')


class Table(models.Model):
    week = models.ForeignKey(Week, blank=False, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, blank=False, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, blank=False, on_delete=models.CASCADE, related_name='player2')
    player1_corp_deck = models.ForeignKey(Deck, blank=False, on_delete=models.CASCADE, related_name='player1_corp')
    player2_runner_deck = models.ForeignKey(Deck, blank=False, on_delete=models.CASCADE, related_name='player2_runner')
    player1_runner_deck = models.ForeignKey(Deck, blank=False, on_delete=models.CASCADE, related_name='player1_runner')
    player2_corp_deck = models.ForeignKey(Deck, blank=False, on_delete=models.CASCADE, related_name='player2_corp')

    def __str__(self):
        return f'{self.week} - {self.player1.name} vs {self.player2.name}'


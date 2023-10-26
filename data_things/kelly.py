p_win = 0.8
p_loss = 1-p_win

win_gain = 0.8
lose_loss = 0.5

kelly = (p_win/lose_loss) - (p_loss/win_gain)

print(kelly)
import streamlit as st
import random
import pandas as pd

# ----------------- CARD LOGIC -----------------
cards = [2,3,4,5,6,7,8,9,10,10,10,10,11]

def deal_card():
    return random.choice(cards)

def calculate_total(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# ----------------- SESSION STATE -----------------
if "player" not in st.session_state:
    st.session_state.player = [deal_card(), deal_card()]
    st.session_state.dealer = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.show_dealer = False
    st.session_state.message = ""
    st.session_state.games_played = 0
    st.session_state.player_wins = 0
    st.session_state.dealer_wins = 0
    st.session_state.ties = 0

# Money and betting
if "player_money" not in st.session_state:
    st.session_state.player_money = 50
    st.session_state.current_bet = 0
    st.session_state.money_history = []

if "lose_messages" not in st.session_state:
    st.session_state.lose_messages = [
        "The house always wins!",
        "Snake eyes huh?",
        "Better luck next time!",
        "Ouch! You're broke!"
    ]

# ----------------- CALLBACK FUNCTIONS -----------------
def start_new_game():
    # Only reset the game state, NOT the current bet
    st.session_state.player = [deal_card(), deal_card()]
    st.session_state.dealer = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.show_dealer = False
    st.session_state.message = ""

    # Reset money if totally broke
    if st.session_state.player_money <= 0:
        st.session_state.player_money = 50
        st.session_state.money_history.clear()
        st.session_state.current_bet = 0

def place_bet(bet):
    # Set the bet and deal new hands
    st.session_state.current_bet = bet
    start_new_game()

def hit():
    st.session_state.player.append(deal_card())
    if calculate_total(st.session_state.player) > 21:
        st.session_state.game_over = True
        st.session_state.message = f"💥 You busted! You lost ${st.session_state.current_bet}"
        st.session_state.player_money -= st.session_state.current_bet
        st.session_state.money_history.append(-st.session_state.current_bet)
        st.session_state.games_played += 1
        st.session_state.dealer_wins += 1
        st.session_state.current_bet = 0  # reset bet for next round

def stand():
    st.session_state.game_over = True

def reveal_dealer():
    while calculate_total(st.session_state.dealer) < 17:
        st.session_state.dealer.append(deal_card())

    player_total = calculate_total(st.session_state.player)
    dealer_total = calculate_total(st.session_state.dealer)

    if dealer_total > 21:
        st.session_state.message = f"🎉 Dealer busted! You win ${st.session_state.current_bet}!"
        st.session_state.player_money += st.session_state.current_bet
        st.session_state.money_history.append(st.session_state.current_bet)
        st.session_state.player_wins += 1
    elif dealer_total > player_total:
        st.session_state.message = f"💥 Dealer wins! You lost ${st.session_state.current_bet}"
        st.session_state.player_money -= st.session_state.current_bet
        st.session_state.money_history.append(-st.session_state.current_bet)
        st.session_state.dealer_wins += 1
    elif dealer_total < player_total:
        st.session_state.message = f"🎉 You win ${st.session_state.current_bet}!"
        st.session_state.player_money += st.session_state.current_bet
        st.session_state.money_history.append(st.session_state.current_bet)
        st.session_state.player_wins += 1
    else:
        st.session_state.message = "🤝 It's a tie!"
        st.session_state.money_history.append(0)
        st.session_state.ties += 1

    st.session_state.show_dealer = True
    st.session_state.games_played += 1
    st.session_state.current_bet = 0  # reset bet for next round

# ----------------- PAGE NAVIGATION -----------------
page = st.sidebar.selectbox("Select Page", ["Game", "Statistics", "About"])

# ----------------- ABOUT PAGE -----------------
if page == "About":
    st.title("Welcome To The House of Hearts!")
    st.markdown("""
    **Features:**
    - Play Blackjack against a computer dealer.
    - Track your game statistics (wins, losses, ties, money) in a data table.
    - Place bets and see your gains/losses.
    - Interactive buttons for Hit, Stand, and revealing the dealer's hand.
    Enjoy the game and may the odds be in your favor! 🎲
    """)

# ----------------- STATISTICS PAGE -----------------
elif page == "Statistics":
    st.title("📊 Game Statistics")
    data = {
        "Games Played": [st.session_state.games_played],
        "Player Wins": [st.session_state.player_wins],
        "Dealer Wins": [st.session_state.dealer_wins],
        "Ties": [st.session_state.ties],
        "Current Money": [st.session_state.player_money],
        "Net Gain/Loss": [sum(st.session_state.money_history)]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("💹 Money History Per Game")
    if st.session_state.money_history:
        history_df = pd.DataFrame({
            "Game": list(range(1, len(st.session_state.money_history) + 1)),
            "Change": st.session_state.money_history
        })
        st.dataframe(history_df)
    else:
        st.write("No games played yet!")

# ----------------- MAIN GAME PAGE -----------------
else:
    st.title("🃏 Blackjack")

    # Show current money
    st.subheader(f"💰 Money: ${st.session_state.player_money}")

    # ----------------- BETTING -----------------
    if st.session_state.player_money > 0 and st.session_state.current_bet == 0:
        bet = st.number_input(
            "Enter your bet:",
            min_value=1,
            max_value=st.session_state.player_money,
            step=1
        )
        st.button("Place Bet", on_click=lambda: place_bet(bet))
        st.stop()  # wait until bet is placed

    # Player broke
    if st.session_state.player_money <= 0:
        st.subheader(random.choice(st.session_state.lose_messages))
        st.button("New Game", on_click=start_new_game)
        st.stop()

    # ----------------- CSS -----------------
    st.markdown("""
    <style>
    .card-table {
        background-color:#1f7a3f;
        padding:20px;
        border-radius:12px;
        margin-bottom:15px;
    }
    .card {
        display:inline-block;
        background-color:white;
        color:black;
        font-weight:bold;
        padding:10px 15px;
        margin-right:5px;
        border-radius:8px;
        min-width:30px;
        text-align:center;
    }
    .buttons-container {
        margin-top:10px;
        text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- DEALER -----------------
    st.markdown("<div class='card-table'>", unsafe_allow_html=True)
    st.subheader("Dealer's hand")
    dealer_cards = ""
    if st.session_state.show_dealer:
        dealer_cards = " ".join([f"<div class='card'>{c}</div>" for c in st.session_state.dealer])
        st.markdown(f"{dealer_cards} Total: {calculate_total(st.session_state.dealer)}", unsafe_allow_html=True)
    else:
        dealer_cards = f"<div class='card'>{st.session_state.dealer[0]}</div> <div class='card'>?</div>"
        st.markdown(f"{dealer_cards} Total: ?", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- PLAYER -----------------
    st.markdown("<div class='card-table'>", unsafe_allow_html=True)
    st.subheader("Player's hand")
    player_cards = " ".join([f"<div class='card'>{c}</div>" for c in st.session_state.player])
    st.markdown(f"{player_cards} Total: {calculate_total(st.session_state.player)}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- BUTTONS -----------------
    st.markdown("<div class='buttons-container'>", unsafe_allow_html=True)
    if not st.session_state.game_over:
        col1, col2 = st.columns(2)
        col1.button("Hit", on_click=hit)
        col2.button("Stand", on_click=stand)
    elif not st.session_state.show_dealer:
        st.button("Reveal Dealer Hand", on_click=reveal_dealer)
    else:
        st.button("New Game", on_click=start_new_game)
    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------- MESSAGE -----------------
    if st.session_state.message:
        st.subheader(st.session_state.message)

    # ----------------- MONEY HISTORY -----------------
    st.subheader("💹 Money History")
    st.write(st.session_state.money_history)

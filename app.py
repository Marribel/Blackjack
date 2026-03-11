import streamlit as st
import random

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

def start_new_game():
    st.session_state.player = [deal_card(), deal_card()]
    st.session_state.dealer = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.show_dealer = False
    st.session_state.message = ""

# ----------------- PAGE NAVIGATION -----------------
page = st.sidebar.selectbox("Select Page", ["Game", "Statistics", "About"])

# ----------------- ABOUT PAGE -----------------
if page == "About":
    st.title("🃏 About This Blackjack Game")
    st.markdown("""
    Welcome to this simple Blackjack game made with **Streamlit**!  

    **Features:**
    - Play Blackjack against a computer dealer.
    - Track your game statistics (wins, losses, ties).
    - Interactive buttons for Hit, Stand, and revealing the dealer's hand.
    - Simple card table style using CSS.

    Enjoy the game and may the odds be in your favor! 🎲
    """)

# ----------------- STATISTICS PAGE -----------------
elif page == "Statistics":
    st.title("📊 Game Statistics")
    st.markdown(f"""
    **Games Played:** {st.session_state.games_played}  
    **Player Wins:** {st.session_state.player_wins}  
    **Dealer Wins:** {st.session_state.dealer_wins}  
    **Ties:** {st.session_state.ties}  
    """)

# ----------------- MAIN GAME PAGE -----------------
else:
    st.title("🃏 Blackjack")

    # CSS for card tables
    st.markdown("""
    <style>
    .card-table {
        background-color:#1f7a3f;
        padding:20px;
        border-radius:12px;
        margin-bottom:15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Button logic
    col1, col2 = st.columns(2)
    if not st.session_state.game_over:
        if col1.button("Hit"):
            st.session_state.player.append(deal_card())
            if calculate_total(st.session_state.player) > 21:
                st.session_state.game_over = True
                st.session_state.message = "💥 You busted!"
                st.session_state.games_played += 1
                st.session_state.dealer_wins += 1

        if col2.button("Stand"):
            st.session_state.game_over = True

    elif not st.session_state.show_dealer:
        if st.button("Reveal Dealer Hand"):
            while calculate_total(st.session_state.dealer) < 17:
                st.session_state.dealer.append(deal_card())

            player_total = calculate_total(st.session_state.player)
            dealer_total = calculate_total(st.session_state.dealer)

            if dealer_total > 21:
                st.session_state.message = "🎉 Dealer busted! You win!"
                st.session_state.player_wins += 1
            elif dealer_total > player_total:
                st.session_state.message = "💥 Dealer wins!"
                st.session_state.dealer_wins += 1
            elif dealer_total < player_total:
                st.session_state.message = "🎉 You win!"
                st.session_state.player_wins += 1
            else:
                st.session_state.message = "🤝 It's a tie!"
                st.session_state.ties += 1

            st.session_state.show_dealer = True
            st.session_state.games_played += 1

    else:
        if st.button("New Game"):
            start_new_game()

    # Dealer hand display
    st.markdown("<div class='card-table'>", unsafe_allow_html=True)
    st.subheader("Dealer's hand")
    if st.session_state.show_dealer:
        st.write(st.session_state.dealer, "Total:", calculate_total(st.session_state.dealer))
    else:
        st.write([st.session_state.dealer[0], "?"], "Total: ?")
    st.markdown("</div>", unsafe_allow_html=True)

    # Player hand display
    st.markdown("<div class='card-table'>", unsafe_allow_html=True)
    st.subheader("Player's hand")
    st.write(st.session_state.player, "Total:", calculate_total(st.session_state.player))
    st.markdown("</div>", unsafe_allow_html=True)

    # Message display
    if st.session_state.message:
        st.subheader(st.session_state.message)

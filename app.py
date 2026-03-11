import streamlit as st
import random

# Cards: 10 represents face cards, 11 represents Ace
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

def deal_card():
    return random.choice(cards)

def calculate_total(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# Initialize game state
if "player" not in st.session_state:
    st.session_state.player = [deal_card(), deal_card()]
    st.session_state.dealer = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.message = ""

def start_new_game():
    st.session_state.player = [deal_card(), deal_card()]
    st.session_state.dealer = [deal_card(), deal_card()]
    st.session_state.game_over = False
    st.session_state.message = ""

if not st.session_state.player:
    start_new_game()

st.title("🃏 Blackjack 1")
def colored_container(content, color="#f0f0f5"):
    with st.container():
        st.markdown(
            f"<div style='background-color:{color}; padding:10px; border-radius:8px'>{content}</div>",
            unsafe_allow_html=True,
        )
# Used containers for clarity
dealer_container = st.container()
player_container = st.container()
message_container = st.container()
buttons_container = st.container()

# Show dealer hand
with dealer_container:
    st.subheader("Dealer's hand:")
    if st.session_state.game_over:
        st.write(st.session_state.dealer, "Total:", calculate_total(st.session_state.dealer))
    else:
        st.write([st.session_state.dealer[0], "?"], "Total: ?")

# Show player hand
with player_container:
    st.subheader("Player's hand:")
    st.write(st.session_state.player, "Total:", calculate_total(st.session_state.player))

# Buttons
with buttons_container:
    if not st.session_state.game_over:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Hit"):
                st.session_state.player.append(deal_card())
                if calculate_total(st.session_state.player) > 21:
                    st.session_state.game_over = True
                    st.session_state.message = "💥 You busted! Dealer wins."
                st.rerun()

        with col2:
            if st.button("Stand"):
                # Dealer plays
                while calculate_total(st.session_state.dealer) < 17:
                    st.session_state.dealer.append(deal_card())
                player_total = calculate_total(st.session_state.player)
                dealer_total = calculate_total(st.session_state.dealer)
                if dealer_total > 21:
                    st.session_state.message = "🎉 Dealer busted! You win!"
                elif dealer_total > player_total:
                    st.session_state.message = "💥 Dealer wins!"
                elif dealer_total < player_total:
                    st.session_state.message = "🎉 You win!"
                else:
                    st.session_state.message = "🤝 It's a tie!"
                st.session_state.game_over = True
    else:
        if st.button("New Game"):
            start_new_game()

# Show message after game ends
with message_container:
    if st.session_state.message:
        st.subheader(st.session_state.message)
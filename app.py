import streamlit as st
from blockchain import Blockchain

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.set_page_config(page_title="💰 EduCoin Classroom", layout="wide")
st.title("💰 Classroom Cryptocurrency (EduCoin)")

# Top metrics
st.subheader("📊 Metrics")
users = list(set([b.sender for b in st.session_state.blockchain.chain] +
                 [b.receiver for b in st.session_state.blockchain.chain]))
users = [u for u in users if u != "System"]
st.metric("Total Users", len(users))
st.metric("Total Transactions", len(st.session_state.blockchain.chain) - 1)

# Teacher reward section
st.subheader("🏆 Teacher Reward Coins")
teacher_name = st.text_input("Teacher Name", key="teacher")
student_name = st.text_input("Student Name to reward", key="reward_student")
if st.button("Reward 1 Coin"):
    if teacher_name.strip() and student_name.strip():
        st.session_state.blockchain.add_block(sender=teacher_name, receiver=student_name, amount=1)
        st.success(f"1 EduCoin rewarded to {student_name} by {teacher_name}!")
    else:
        st.warning("Enter both teacher and student names.")

# Student transaction section
st.subheader("💸 Transfer Coins Between Students")
sender = st.text_input("Sender Name", key="sender")
receiver = st.text_input("Receiver Name", key="receiver")
amount = st.number_input("Amount to Transfer", min_value=1, step=1, key="amount")
if st.button("Send Coins"):
    if sender.strip() and receiver.strip() and amount > 0:
        balance = st.session_state.blockchain.get_balance(sender)
        if balance >= amount:
            st.session_state.blockchain.add_block(sender=sender, receiver=receiver, amount=amount)
            st.success(f"{amount} EduCoins transferred from {sender} to {receiver}!")
        else:
            st.error(f"Insufficient balance! {sender} has {balance} coins.")
    else:
        st.warning("Fill all fields correctly.")

# Verify blockchain
if st.button("🔒 Verify Blockchain"):
    if st.session_state.blockchain.verify_chain():
        st.success("✅ Blockchain is valid.")
    else:
        st.error("❌ Blockchain integrity compromised!")

# Leaderboard
st.subheader("🏅 Leaderboard")
leaderboard = st.session_state.blockchain.get_leaderboard()
if leaderboard:
    for rank, (user, bal) in enumerate(leaderboard, 1):
        st.write(f"{rank}. {user} — {bal} EduCoins")
else:
    st.info("No student transactions yet.")

# Transaction history
st.subheader("📜 Transaction History")
for block in reversed(st.session_state.blockchain.chain):
    if block.index == 0:
        continue  # skip genesis
    with st.expander(f"Txn {block.transaction_id} | {block.sender} → {block.receiver}", expanded=False):
        st.write(f"Amount: {block.amount}")
        st.write(f"Timestamp: {block.timestamp}")
        st.write(f"Hash: {block.hash}")
        st.write(f"Previous Hash: {block.previous_hash}")

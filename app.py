import streamlit as st
from blockchain import Blockchain

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.set_page_config(page_title="💰 EduCoin Classroom", layout="wide")
st.title("💰 Classroom Cryptocurrency (EduCoin)")

# Metrics
users = list(set([b.sender for b in st.session_state.blockchain.chain] +
                 [b.receiver for b in st.session_state.blockchain.chain]))
users = [u for u in users if u != "System"]

st.subheader("📊 Metrics")
st.metric("Total Users", len(users))
st.metric("Total Transactions", len(st.session_state.blockchain.chain) - 1)

# ---------------- Balance Check ----------------
st.subheader("💰 Check EduCoin Balance")
check_user = st.text_input("Enter Name to check balance", key="balance_check")
if check_user.strip():
    balance = st.session_state.blockchain.get_balance(check_user)
    st.info(f"💵 {check_user} has {balance} EduCoins")

# ---------------- Teacher Reward ----------------
st.subheader("🏆 Teacher Reward Coins")
teacher_name_reward = st.text_input("Teacher Name", key="teacher_reward")
student_name_reward = st.text_input("Student Name to reward", key="student_reward")
if st.button("Reward 1 Coin"):
    if teacher_name_reward.strip() and student_name_reward.strip():
        st.session_state.blockchain.add_block(sender=teacher_name_reward, receiver=student_name_reward, amount=1)
        st.success(f"1 EduCoin rewarded to {student_name_reward} by {teacher_name_reward}")
    else:
        st.warning("Enter both teacher and student names.")

# ---------------- Mint Coins ----------------
st.subheader("🪙 Mint Coins (Add Money)")
teacher_name_mint = st.text_input("Teacher Name for Minting", key="teacher_mint")
student_name_mint = st.text_input("Student Name to Add Coins", key="student_mint")
mint_amount = st.number_input("Amount to Add", min_value=1, step=1, key="mint_amount")
if st.button("Mint Coins"):
    if teacher_name_mint.strip() and student_name_mint.strip() and mint_amount > 0:
        st.session_state.blockchain.add_block(sender=teacher_name_mint, receiver=student_name_mint, amount=mint_amount)
        st.success(f"{mint_amount} EduCoins added to {student_name_mint} by {teacher_name_mint}")
    else:
        st.warning("Enter all fields correctly.")

# ---------------- Student Transfer ----------------
st.subheader("💸 Transfer Coins Between Students")
sender_name = st.text_input("Sender Name", key="sender_transfer")
receiver_name = st.text_input("Receiver Name", key="receiver_transfer")
transfer_amount = st.number_input("Amount to Transfer", min_value=1, step=1, key="transfer_amount")
if st.button("Send Coins"):
    if sender_name.strip() and receiver_name.strip() and transfer_amount > 0:
        sender_balance = st.session_state.blockchain.get_balance(sender_name)
        if sender_balance >= transfer_amount:
            st.session_state.blockchain.add_block(sender=sender_name, receiver=receiver_name, amount=transfer_amount)
            st.success(f"{transfer_amount} EduCoins transferred from {sender_name} to {receiver_name}")
        else:
            st.error(f"Insufficient balance! {sender_name} has {sender_balance} coins.")
    else:
        st.warning("Fill all fields correctly.")

# ---------------- Verify Blockchain ----------------
st.subheader("🔒 Verify Blockchain Integrity")
if st.button("Verify Blockchain"):
    if st.session_state.blockchain.verify_chain():
        st.success("✅ Blockchain is valid")
    else:
        st.error("❌ Blockchain integrity compromised!")

# ---------------- Leaderboard ----------------
st.subheader("🏅 Leaderboard")
leaderboard = st.session_state.blockchain.get_leaderboard()
if leaderboard:
    for rank, (user, bal) in enumerate(leaderboard, 1):
        st.write(f"{rank}. {user} — {bal} EduCoins")
else:
    st.info("No transactions yet.")

# ---------------- Transaction History ----------------
st.subheader("📜 Transaction History")
for block in reversed(st.session_state.blockchain.chain):
    if block.index == 0:
        continue
    with st.expander(f"Txn {block.transaction_id} | {block.sender} → {block.receiver}", expanded=False):
        st.write(f"Amount: {block.amount}")
        st.write(f"Timestamp: {block.timestamp}")
        st.write(f"Hash: {block.hash}")
        st.write(f"Previous Hash: {block.previous_hash}")

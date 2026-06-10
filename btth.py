import logging

class InvalidAmountError(Exception):
    """Lỗi số tiền không hợp lệ."""
    pass


class InsufficientBalanceError(Exception):
    """Lỗi số dư không đủ."""
    pass

class Wallet:
    """
    Quản lý ví điện tử.
    Attributes:
        balance (int): Số dư hiện tại.
    """
    def __init__(self):
        """
        Khởi tạo ví.
        Returns:
            None
        """
        self.balance = 0
    def deposit(self, amount):
        """
        Nạp tiền vào ví.
        Args:
            amount (int): Số tiền cần nạp.
        Returns:
            None
        Raises:
            InvalidAmountError
        """
        if amount <= 0:
            raise InvalidAmountError
        self.balance += amount
        logging.info(f"Deposit successful: +{amount} VND. Current Balance: {self.balance}")
    def transfer(self, phone, amount):
        """
        Chuyển tiền.
        Args:
            phone (str): Số điện thoại nhận.
            amount (int): Số tiền chuyển.
        Returns:
            None
        Raises:
            InvalidAmountError
            InsufficientBalanceError
        """
        if amount <= 0:
            raise InvalidAmountError
        if amount > self.balance:
            raise InsufficientBalanceError
        if amount >= 10000000:
            logging.warning(
                f"High value transaction detected: {amount} VND to {phone}"
            )
        self.balance -= amount
        logging.info(f"Transfer successful: -{amount} VND to {phone}. Current Balance: {self.balance}")
    def get_balance(self):
        """
        Lấy số dư hiện tại.
        Returns:
            int
        """
        return self.balance

def input_amount(message):
    """
    Nhập số tiền hợp lệ.
    Args:
        message (str)
    Returns:
        int
    """
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")
            logging.error("ValueError: Invalid numeric input.")

def deposit_money(wallet):
    """
    Chức năng nạp tiền.
    Args:
        wallet (Wallet)
    Returns:
        None
    """
    print("\n--- NẠP TIỀN VÀO VÍ ---")
    try:
        amount = input_amount("Nhập số tiền cần nạp: ")
        wallet.deposit(amount)
        print(f"Nạp tiền thành công: +{amount:,} VND")
        print(f"Số dư hiện tại: {wallet.get_balance():,} VND")
    except InvalidAmountError:
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")
        logging.error(
            f"InvalidAmountError: Attempted to process {amount} VND."
        )

def transfer_money(wallet):
    """
    Chức năng chuyển tiền.
    Args:
        wallet (Wallet)
    Returns:
        None
    """
    print("\n--- CHUYỂN TIỀN ---")
    phone = input("Nhập số điện thoại người nhận: ").strip()
    amount = input_amount("Nhập số tiền cần chuyển: ")
    try:
        wallet.transfer(phone, amount)
        print(f"Chuyển tiền thành công tới số điện thoại {phone}.")
        print(f"Số tiền đã chuyển: {amount:,} VND")
        print(f"Số dư còn lại: {wallet.get_balance():,} VND")

    except InvalidAmountError:
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")
        logging.error(f"InvalidAmountError: Attempted to process {amount} VND.")
    except InsufficientBalanceError:
        print("Giao dịch thất bại: Số dư của bạn không đủ.")
        print(f"Số dư hiện tại: {wallet.get_balance():,} VND")
        logging.error(
            f"InsufficientBalanceError: Attempted to transfer {amount} VND "
            f"with balance {wallet.get_balance()} VND.")

def show_logs():
    """
    Hiển thị 5 log gần nhất.

    Returns:
        None
    """
    print("\n--- 5 SỰ KIỆN GẦN NHẤT TRONG HỆ THỐNG ---")
    try:
        with open(
            "momo_transactions.log",
            "r",
            encoding="utf-8"
        ) as file:
            logs = file.readlines()
        for log in logs[-5:]:
            print(log.strip())
    except FileNotFoundError:
        print("Chưa có lịch sử giao dịch nào trong hệ thống.")


def show_balance(wallet):
    """
    Hiển thị số dư.
    Args:
        wallet (Wallet)
    Returns:
        None
    """
    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(f"Số dư hiện tại: {wallet.get_balance():,} VND")
    logging.info(f"Balance checked. Current Balance: {wallet.get_balance()}")


def main():
    logging.basicConfig(
        filename="momo_transactions.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        encoding="utf-8"
    )
    wallet = Wallet()
    while True:
        print("""
========== VÍ MOMO GIẢ LẬP ==========
1. Nạp tiền vào ví
2. Chuyển tiền
3. Xem lịch sử hệ thống
4. Xem số dư tài khoản
5. Thoát chương trình
====================================""")
        choice = input("Chọn chức năng (1-5): ")
        match choice:
            case "1":
                deposit_money(wallet)
            case "2":
                transfer_money(wallet)
            case "3":
                show_logs()
            case "4":
                show_balance(wallet)
            case "5":
                logging.info("System shutdown")
                print("Cảm ơn bạn đã sử dụng dịch vụ.")
                break
            case _:
                print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
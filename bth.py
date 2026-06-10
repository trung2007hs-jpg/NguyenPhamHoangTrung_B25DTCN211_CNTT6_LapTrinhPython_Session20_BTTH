import logging

ticket_db = [
    {"ticket_id": "T01", "buyer_name": "Nguyen Van A", "price": 500.0, "status": "Booked", "seat": ("A", 1)},
    {"ticket_id": "T02", "buyer_name": "Tran Thi B", "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},
    {"ticket_id": "T03", "buyer_name": "Le Van C", "price": 500.0, "status": "Booked", "seat": ("A", 2)}
]

def display_tickets(tickets):
    if not tickets:
        print('Hiện chưa có vé nào trong hệ thống.')
        return
    print('--- DANH SÁCH VÉ ---')
    print('-'*70)
    print(f"{'Mã Vé':<6} | {'Khách hàng':<20} | {'Giá Vé':<8} | {'Chỗ Ngồi':<10} | {'Trạng Thái':<15}")
    print('-'*70)
    try:
        for ticket in tickets:
            seat = f"{ticket['seat'][0]}-{ticket['seat'][1]}"
            if ticket['status'] == "Cancelled":
                ticket['status'] += ' [ĐÃ HỦY]'
            print(f"{ticket['ticket_id']:<6} | {ticket['buyer_name']:<20} | {ticket['price']:<8} | {seat:<10} | {ticket['status']:<15}")
            cheak_viewed = True
    except KeyError:
        print('Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.')
    if cheak_viewed:
        logging.info('User viewed ticket list')
    else:
        logging.error("Missing key while displaying ticket: 'seat'")
    print('-'*70)
    
def check_ticket_exits(tickets, ticket_id):
    for ticket in tickets:
        if ticket_id.strip().upper() == ticket['ticket_id']:
            return ticket
    return

def input_format_int(message):
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print('Giá vé phải lớn hơn 0, vui lòng nhập lại ')
            return value
        except ValueError:
            print('Giá vé phải là số, vui lòng nhập lại')
            logging.warning('Invalid price input while booking ticket')
    
def book_ticket(tickets):
    print('--- ĐẶT VÉ MỚI ---')
    ticket_id = input('Nhập mã vé: ').strip().upper()
    ticket = check_ticket_exits(tickets, ticket_id)
    if ticket is not None:
        print(f'Lỗi: Mã vé {ticket_id} đã tồn tại')
        logging.warning(f'Duplicate ticket ID entered: {ticket_id}')
        return
    buyer_name = input('Nhập tên khách hàng: ').strip().title()
    if not buyer_name:
        print('Tên khách hàng không để trống')
        return
    price = input_format_int('Nhập giá vé: ')
    ticket_zone = input('Nhập khu vực ghế: ').upper()
    if not ticket_zone:
        print('Khu vé không để trống')
        return    
    try:
        seet_quantity = int(input('Nhập khu số ghế: '))
        if seet_quantity <= 0:
            print('Số ghế phải là số dương, vui lòng nhập lại ')
            return
    except ValueError:
        print('Phải nhập số')
        return
    seet = (ticket_zone, seet_quantity)
    tickets.append({
        'ticket_id': ticket_id,
        'buyer_name': buyer_name,
        'price': price,
        'seet': seet,
        'status': 'Booked'
    })
    print(f'Thành công: Đã đặt vé {ticket_id} cho khách hàng {buyer_name}.')
    logging.info(f'Booked new ticket {ticket_id} for {buyer_name}')
      
def change_seat(tickets):
    print('--- ĐỔI CHỖ NGỒI ---')
    ticket_id = input('Nhập mã vé cần đổi mới: ').strip().upper()
    ticket = check_ticket_exits(tickets, ticket_id)
    if ticket is None:
        print(f'Không tìm thấy vé mang mã {ticket_id}')
        logging.warning(f'Change seat failed - Ticket {ticket_id} not found')
        return
    ticket_zone = input('Nhập khu vực ghế: ').upper()
    if not ticket_zone:
        print('Khu vé không để trống')
        return   
    try:
        seet_quantity = int(input('Nhập khu vực ghế: '))
        if seet_quantity <= 0:
            print('Số ghế phải là số dương, vui lòng nhập lại ')
            return
    except ValueError:
        print('Phải nhập số')
        return
    ticket['seat'] = (ticket_zone, seet_quantity)
    print(f'Thành công: Đã đổi chỗ vé {ticket_zone} sang {ticket_zone}-{seet_quantity}')
    logging.info(f'Seat changed for ticket {ticket_zone} to {ticket_zone}-{seet_quantity}')
    
def cancel_ticket(tickets):
    print('--- HỦY VÉ ---')
    ticket_id = input('Nhập mã vé cần đổi mới: ').strip().upper()
    ticket = check_ticket_exits(tickets, ticket_id)
    if ticket is None:
        print(f'Không tìm thấy vé mang mã {ticket_id}')
        logging.warning(f'Cancel ticket failed - Ticket {ticket_id} not found')
        return
    if ticket['status'] == 'Cancelled':
        print(f'Vé {ticket_id} đã ở trạng thái Cancelled trước đó')
        return
    if ticket['status'] == 'Booked':
        ticket['status'] == 'Cancelled'
        print(f'Thành công: Vé {ticket_id} đã được hủy')
        logging.warning(f'Ticket {ticket_id} has been cancelled')
        
def calculate_revenue(tickets):
    total_revenue = 0
    booked = 0
    cancelled = 0
    for ticket in tickets:
        if ticket['status'] == 'Booked':
            total_revenue += ticket['price']
            booked += 1
        elif ticket['status'] == 'Cancelled':
            cancelled += 1
    print(f'''--- BÁO CÁO DOANH THU ---
Tổng số vé đã đặt: {booked}
Tổng số vé đã hủy: {cancelled}
Tổng doanh thu hợp lệ: {total_revenue:,}''')
    logging.info(f'Revenue report generated. Total: {total_revenue}')
    return {
        'booked': booked,
        'cancelled': cancelled,
        'revenue': total_revenue
    }
            
     
def main():
    logging.basicConfig(
        filename='Bài tổng hợp.txt',
        format= '%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        encoding='utf-8'
    )
    while True:
        print("""
=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===
1. Xem danh sách vé đã bán
2. Đặt vé mới
3. Đổi chỗ ngồi (Cập nhật vé)
4. Hủy vé
5. Báo cáo doanh thu
6. Thoát chương trình
======================================== """)
        choice = input('Chọn chức năng (1-6): ')
        match choice:
            case '1':
                display_tickets(ticket_db)
            case '2':
                book_ticket(ticket_db)
            case '3':
                change_seat(ticket_db)
            case '4':
                cancel_ticket(ticket_db)
            case '5':
                calculate_revenue(ticket_db)
            case '6':
                print('Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.')
                break
            case _:
                print('Lựa chọn không hợp lệ.')

if __name__ == '__main__':
    main()        
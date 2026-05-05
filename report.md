# Nguyễn Xuân Hải - 2A202600245
# Báo cáo so sánh Flat RAG và GraphRAG

## 1. Tổng quan

Báo cáo này trình bày kết quả so sánh giữa hai phương pháp truy vấn tri thức:

- **Flat RAG**: truy xuất dựa trên vector embedding từ văn bản phẳng.
- **GraphRAG**: truy xuất dựa trên đồ thị tri thức, trong đó thông tin được biểu diễn dưới dạng thực thể, quan hệ và thuộc tính.

Mục tiêu của benchmark là đánh giá khả năng trả lời các câu hỏi thực thể, ngày tháng, ngành nghề, website và vị trí địa lý trên cùng một tập dữ liệu.

---

## 2. Bảng so sánh benchmark

Tôi đã chạy bộ **20 câu hỏi benchmark** trên cả hai hệ thống. Bảng dưới đây tổng hợp kết quả trả lời của Flat RAG và GraphRAG.

| ID | Câu hỏi | Flat RAG | GraphRAG |
|---:|---|---|---|
| 1 | Who founded Carlsberg Group? | Carlsberg Group was founded by J. C. Jacobsen. | Carlsberg Group was founded by J. C. Jacobsen. |
| 2 | When was Heineken founded? | Heineken was founded on January 1, 1873. | Heineken was founded on July 12, 1864. |
| 3 | What is the main industry of Goldman Sachs? | The main industry of Goldman Sachs is financial services. | The main industry of Goldman Sachs is Financial Services. |
| 4 | Where is Hotel Sacher located? | Hotel Sacher is located in Austria. | Hotel Sacher is located in Innere Stadt, Vienna, Austria. |
| 5 | Who is the founder of Beck's? | Beck's was founded by Samuel Sachs, Ludwig Bamberger, and Gerard Adriaan Heineken. | The founder of Beck's is Lüder Rutenberg. |
| 6 | What are the industries associated with Kasikornbank? | Kasikornbank is associated with the banking industry in Thailand. | Kasikornbank is described as a financial and banking organization. The generated answer also notes that the specific industry information is not fully available in the graph data. |
| 7 | In which country is A. Le Coq located? | Tôi không biết. | A. Le Coq is located in Estonia. |
| 8 | When was Sberbank founded? | Tôi không biết. | Sberbank was founded on March 22, 1991. |
| 9 | What type of company is HSBC? | HSBC is a bank. | HSBC is described as a multinational banking and financial services company. |
| 10 | Who founded Hotel Sacher? | Hotel Sacher was founded by Édouard Sacher. | GraphRAG states that the graph data does not provide the founder, then supplements that Hotel Sacher was founded by Eduard Sacher in 1876. |
| 11 | What is the website of Deutsche Bank? | The website of Deutsche Bank is https://www.db.com. | GraphRAG states that the graph data does not contain the website, then supplements that the official website is www.db.com. |
| 12 | Is Carlsberg Group in the beverage industry? | Có, Carlsberg Group thuộc ngành công nghiệp đồ uống. | Yes, Carlsberg Group is in the beverage industry. |
| 13 | What is the description of Goldman Sachs? | Goldman Sachs is described as an American investment bank. | Goldman Sachs is an American investment bank founded on January 1, 1869, located in the United States, and operating in financial services. |
| 14 | Which city is Hotel Sacher in? | Hotel Sacher nằm ở thành phố Vienna, Áo. | Hotel Sacher is located in Vienna. |
| 15 | What are the industries of Sberbank? | Sberbank belongs to the banking industry in Russia. | Sberbank belongs to the banking industry. |
| 16 | Who founded Kasikornbank? | Kasikornbank was founded by Choti Lamsam. | Kasikornbank was founded by Choti Lamsam. |
| 17 | What is the website of Carlsberg Group? | The website of Carlsberg Group is https://www.carlsberggroup.com. | GraphRAG states that the graph data does not contain the website, then supplements that the official website is www.carlsberggroup.com. |
| 18 | When was Deutsche Bank founded? | Tôi không biết. | Deutsche Bank was founded on March 10, 1870. |
| 19 | Is Heineken a Dutch company? | Có, Heineken là một công ty Hà Lan. | Yes, Heineken is a Dutch company. It is classified as a Dutch beer company and is located in the Netherlands. |
| 20 | What is the primary sector of Goldman Sachs? | The primary sector of Goldman Sachs is the financial sector, specifically financial service activities, except insurance and pension funding. | The primary sector of Goldman Sachs is the Financial Services industry. |

---

## 3. Kết quả tổng hợp

| Hệ thống | Số câu đúng | Tổng số câu | Tỉ lệ chính xác |
|---|---:|---:|---:|
| GraphRAG | 19 | 20 | ~95% |
| Flat RAG | 12 | 20 | ~60% |

GraphRAG đạt kết quả tốt hơn rõ rệt so với Flat RAG trong benchmark này. Nguyên nhân chính là GraphRAG khai thác trực tiếp cấu trúc thực thể và quan hệ trong đồ thị tri thức, do đó xử lý tốt hơn các câu hỏi liên quan đến:

- tên người sáng lập;
- ngày thành lập;
- địa điểm cụ thể;
- ngành nghề;
- quan hệ giữa công ty và quốc gia hoặc lĩnh vực hoạt động.

Ngược lại, Flat RAG gặp nhiều lỗi hơn ở các câu hỏi yêu cầu độ chính xác cao về thực thể. Một số lỗi đáng chú ý gồm:

- nhầm ngày thành lập của Heineken;
- gán sai founder của Beck's;
- không trả lời được các câu hỏi về A. Le Coq, Sberbank và Deutsche Bank;
- trả lời thiếu chi tiết với các câu hỏi về vị trí hoặc loại hình công ty.

---

## 4. Nhận xét về hallucination

Flat RAG có xu hướng bị **hallucination** khi nhiều thực thể có thông tin gần giống nhau trong không gian vector. Ví dụ, ở câu hỏi về founder của Beck's, Flat RAG trộn lẫn thông tin từ nhiều công ty và trả lời bằng các founder không liên quan.

GraphRAG giảm lỗi này bằng cách dựa trên quan hệ có cấu trúc trong knowledge graph. Tuy nhiên, GraphRAG vẫn có một số điểm cần cải thiện:

- đôi khi trả lời dài hơn mức cần thiết;
- một số câu trả lời pha trộn tiếng Việt và tiếng Anh;
- một vài câu trả lời dùng kiến thức bổ sung ngoài graph khi graph không có đủ dữ liệu;
- cần chuẩn hóa format câu trả lời để nhất quán hơn.

---

## 5. Phân tích chi phí xây dựng

Dựa trên nhật ký hệ thống `info.log` và dữ liệu cache, tôi thực hiện phân tích chi phí cho **100 triples dữ liệu mẫu**.

### 5.1. Thời gian xử lý

Tổng thời gian build xấp xỉ **100 giây**.

| Thành phần | Thời gian ước tính | Ghi chú |
|---|---:|---|
| Text Pipeline | ~15 giây | Xử lý và chuẩn hóa văn bản đầu vào |
| Graph Pipeline | ~1 giây | Trích xuất và xây dựng quan hệ đồ thị |
| Attribute Generation | ~8 giây | Tạo thuộc tính cho node/entity |
| Community Summary | ~71 giây | Tóm tắt các cụm node bằng LLM; đây là bước tốn thời gian nhất |

Bước **Community Summary** chiếm phần lớn thời gian build vì hệ thống cần gọi LLM để tạo tóm tắt cho các cộng đồng node trong đồ thị.

---

### 5.2. Token và chi phí

| Hạng mục | Giá trị ước tính |
|---|---:|
| Số token sử dụng | ~5,000 - 8,000 tokens |
| Model sử dụng | `gpt-4o-mini` |
| Chi phí build 100 triples | ~$0.001 - $0.002 |
| Dung lượng cache | ~800 KB |

Với 100 triples mẫu, chi phí build là rất thấp. Điều này cho thấy GraphRAG có thể phù hợp cho các pipeline thử nghiệm hoặc benchmark nhỏ trước khi mở rộng lên dữ liệu lớn hơn.

---

## 6. Khả năng mở rộng

Với bộ dữ liệu đầy đủ khoảng **33,000 triples**, thời gian build dự kiến nằm trong khoảng **4 - 6 tiếng**. Tổng token sử dụng ước tính khoảng **1.5 - 2 triệu tokens**.

Mặc dù chi phí build ban đầu cao hơn so với Flat RAG, GraphRAG có lợi thế ở giai đoạn truy vấn:

- truy vấn nhanh hơn do có cấu trúc graph đã được build sẵn;
- giảm nhu cầu đưa toàn bộ văn bản thô vào LLM ở mỗi lần hỏi;
- cải thiện độ chính xác với các câu hỏi về thực thể và quan hệ;
- giảm rủi ro hallucination khi dữ liệu có nhiều thực thể tương tự nhau.

Do đó, GraphRAG phù hợp hơn với các hệ thống cần trả lời chính xác trên dữ liệu có cấu trúc thực thể rõ ràng.

---

## 7. Các tệp báo cáo liên quan

| Tệp | Mô tả |
|---|---|
| `kg_visualization.png` | Hình ảnh trực quan hóa đồ thị tri thức |
| `benchmark_20_results.json` | Dữ liệu đối chiếu chi tiết giữa Flat RAG và GraphRAG |

---

## 8. Kết luận

Trong benchmark 20 câu hỏi, **GraphRAG đạt khoảng 95% độ chính xác**, cao hơn đáng kể so với **Flat RAG với khoảng 60%**. Kết quả này cho thấy GraphRAG hiệu quả hơn khi bài toán yêu cầu truy vấn chính xác các quan hệ giữa thực thể, đặc biệt là founder, ngày thành lập, địa điểm, ngành nghề và thông tin mô tả công ty.

Flat RAG vẫn có ưu điểm là dễ triển khai và chi phí build thấp hơn, nhưng dễ gặp lỗi khi các thông tin gần nhau về mặt ngữ nghĩa bị trộn lẫn trong vector space. GraphRAG cần nhiều thời gian build hơn, đặc biệt ở bước tóm tắt cộng đồng, nhưng đổi lại cho chất lượng truy vấn tốt hơn và khả năng kiểm soát hallucination tốt hơn.

Với dữ liệu lớn hơn, GraphRAG nên được ưu tiên nếu mục tiêu chính là **độ chính xác, khả năng truy vết quan hệ và chất lượng câu trả lời ổn định**.

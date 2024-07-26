# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="TheBloke/NexusRaven-V2-13B-GGUF",
  messages=[
    {"role": "system", "content": "Bạn là trợ lí ảo tóm tắt văn bản. Bạn sẽ tóm tắt văn bản một cách chích xác nhất có thể. Câu trả lời phải theo cấu hình [Ngày đăng: (DD/MM/YY);Tiêu đề: (Tiêu đề);Từ khóa: (từ khóa)]. Từ khóa không dài hơn 2 chữ cái."},
    {"role": "user", "content": "Tôi sẽ cho bạn 1 dây kí tự. Nó được thu thập từ 1 trang báo mạng. Tìm tiêu đề của bài báo, ngày đăng tin và từ khóa chính không dài hơn 16 kí tự. Bỏ qua những văn bản không liên quan.  văn bản: " + '''Văn phòng Trung ương Đảng hôm nay 18.7 đã phát thông báo của Bộ Chính trị về tình hình sức khỏe của Tổng Bí thư Nguyễn Phú Trọng.Thông báo nêu rõ, thời gian qua, theo yêu cầu của Hội đồng chuyên môn bảo vệ sức khỏe cán bộ Trung ương, đồng chíTổng Bí thư Nguyễn Phú Trọngvừa điều hành công việc, vừa điều trị, chăm sóc sức khỏe.Bộ Chính trị ra thông báo về tình hình sức khỏe Tổng Bí thư Nguyễn Phú TrọngVPGBộ Chính trị, Ban Bí thư, các đồng chí lãnh đạo chủ chốt và đồng chí Thường trực Ban Bí thư đã trực tiếp chỉ đạo các cơ quan chuyên môn tập trung huy động đội ngũ các giáo sư, bác sĩ, nhân viên y tế, chuyên gia đầu ngành và những điều kiện thuận lợi nhất để điều trị, chăm sóc sức khỏe cho đồng chí Tổng Bí thư.Bộ Chính trị thông báo tình hình sức khỏe của Tổng Bí thư Nguyễn Phú TrọngBộ Chính trị phân công Chủ tịch nước Tô Lâm chủ trì công việc của Ban Chấp hành Trung ương Đảng, Bộ Chính trị, Ban Bí thưGIA HÂNĐến nay, do yêu cầu cần phải tiếp tục ưu tiên dành thời gian để đồng chí Tổng Bí thư tập trung điều trị tích cực và để bảo đảm công tác điều hành chung của Ban Chấp hành Trung ương Đảng, Bộ Chính trị, Ban Bí thư, căn cứ Quy chế làm việc của Ban Chấp hành Trung ương, Bộ Chính trị và Ban Bí thư khóa XIII, trước mắt Bộ Chính trị phân công đồng chí Tô Lâm, Ủy viên Bộ Chính trị, Chủ tịch nước chủ trì công việc của Ban Chấp hành Trung ương Đảng, Bộ Chính trị, Ban Bí thư theo trách nhiệm, quyền hạn được Bộ Chính trị quy định.Bộ Chính trị kêu gọi toàn Đảng, toàn dân và toàn quân tin tưởng tuyệt đối vào sự lãnh đạo của Đảng, quản lý của Nhà nước, tăng cường đoàn kết, thống nhất, chung sức đồng lòng, tiếp tục phát huy những kết quả, thành tựu quan trọng, toàn diện mà đất nước ta đã đạt được, nỗ lực phấn đấu vượt qua mọi khó khăn, thách thức, hoàn thành tốt các mục tiêu Đại hội Đảng toàn quốc lần thứ XIII đã đề ra; giữ vững ổn định chính trị, bảo vệ vững chắc độc lập, chủ quyền, toàn vẹn lãnh thổ và an ninh quốc gia, trật tự, an toàn xã hội, đẩy mạnh phát triển kinh tế - xã hội, chăm lo tốt đời sống tinh thần, vật chất cho nhân dân.'''}
  ],
  temperature=0.3,
)

print(completion.choices[0].message)
import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const extractText = async () => {
    if (!url) {
      alert("Vui lòng nhập URL");
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch(
        `/extract-text/?url=${encodeURIComponent(url)}`
      );
      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data.results);
      }
    } catch (err) {
      setError("Lỗi khi gọi API: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        margin: "50px",
      }}
    >
      <h2>Trích xuất văn bản từ ảnh trên website</h2>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Nhập URL trang web..."
        style={{ width: "80%", padding: "10px", margin: "10px 0" }}
      />
      <button
        onClick={extractText}
        style={{
          padding: "10px 20px",
          backgroundColor: "#28a745",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        {loading ? "Đang xử lý..." : "Đọc nội dung"}
      </button>

      <div id="result" style={{ marginTop: "20px", textAlign: "left" }}>
        {error && <p style={{ color: "red" }}>Lỗi: {error}</p>}

        {result && (
          <div>
            <h3>Kết quả:</h3>
            {Object.entries(result).map(([imgSrc, text]) => (
              <div key={imgSrc}>
                <p>
                  <strong>Ảnh:</strong>{" "}
                  <a href={imgSrc} target="_blank" rel="noopener noreferrer">
                    {imgSrc}
                  </a>
                </p>
                <p>
                  <strong>Văn bản:</strong>{" "}
                  {text || "Không có văn bản nhận diện được."}
                </p>
                <hr />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

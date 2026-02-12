import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Home() {
    const [url, setUrl] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    function handle(url: string) {
        if (!url) return alert("Enter a repo URL first")

        setLoading(true)

        fetch(`http://localhost:8000/setup?repo_url=${encodeURIComponent(url)}`)
            .then(res => res.json())
            .then((data) => {
                if (data.success) {
                    navigate('/chat')
                } else {
                    alert(`Error => ${data.err}`)
                    setLoading(false)
                }
            })
            .catch(err => {
                alert("Something went wrong")
                console.error(err)
                setLoading(false)
            })
    }

    return (
        <div style={{
            height: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
        }}>
            <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "20px",
                width: "500px",
                textAlign: "center"
            }}>
                <p style={{ fontSize: "22px", fontWeight: 500 }}>
                    Enter the GitHub URL which you want to learn
                </p>

                <input
                    type="text"
                    value={url}
                    onChange={(event) => setUrl(event.target.value)}
                    disabled={loading}
                    style={{
                        padding: "14px",
                        fontSize: "18px",
                        borderRadius: "8px",
                        border: "1px solid #ccc"
                    }}
                />

                <button 
                    onClick={() => handle(url)} 
                    disabled={loading}
                    style={{
                        padding: "14px",
                        fontSize: "20px",
                        borderRadius: "8px",
                        cursor: "pointer"
                    }}
                >
                    {loading ? "Loading..." : "GO"}
                </button>

                {loading && (
                    <div style={{
                        fontSize: "26px",
                        fontWeight: 600,
                        marginTop: "10px"
                    }}>
                        Processing Repo..
                    </div>
                )}
            </div>
        </div>
    )
}

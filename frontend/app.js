const API = "http://127.0.0.1:8000"

let userLocation = {
    lat: null,
    lng: null
}

let currentDoctor = null
let currentHospital = null

/* =========================
   FOLLOWUP SYSTEM
========================= */

let symptomConversation = []
let followupStage = 0
let pendingSymptom = ""

/* =========================
   GPS LOCATION
========================= */

if (navigator.geolocation) {

    navigator.geolocation.getCurrentPosition(

        async (pos) => {

            userLocation.lat = pos.coords.latitude
            userLocation.lng = pos.coords.longitude

            loadCityName()
        },

        () => {
            console.log("Location denied")
        }
    )
}

/* =========================
   AUTH SWITCH
========================= */

function showSignup() {

    const signup = document.getElementById("signupBox")
    const login  = document.getElementById("loginBox")

    if (signup) signup.style.display = "block"
    if (login)  login.style.display  = "none"
}

function showLogin() {

    const signup = document.getElementById("signupBox")
    const login  = document.getElementById("loginBox")

    if (signup) signup.style.display = "none"
    if (login)  login.style.display  = "block"
}

/* =========================
   SIGNUP
========================= */

async function signup() {

    const username = document.getElementById("signupUsername").value.trim()
    const email    = document.getElementById("signupEmail").value.trim()
    const password = document.getElementById("signupPassword").value.trim()

    if (!username || !email || !password) {
        alert("All fields required")
        return
    }

    try {

        const res = await fetch(`${API}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        })

        const data = await res.json()

        if (!res.ok) {
            alert(data.detail || "Signup failed")
            return
        }

        // Auto-login immediately — clear any old session first
        localStorage.clear()
        localStorage.setItem("user_id",  data.id)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email",    data.email)

        window.location.replace("/chatpage")

    } catch {
        alert("Signup failed")
    }
}

/* =========================
   LOGIN
========================= */

async function login() {

    const email    = document.getElementById("loginEmail").value.trim()
    const password = document.getElementById("loginPassword").value.trim()

    if (!email || !password) {
        alert("All fields required")
        return
    }

    try {

        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        })

        const data = await res.json()

        if (!res.ok) {
            alert(data.detail || "Login failed")
            return
        }

        // Clear any previous user's session data FIRST before writing new user
        localStorage.clear()

        localStorage.setItem("user_id",  data.id)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email",    data.email)

        window.location.replace("/chatpage")

    } catch {
        alert("Login failed")
    }
}

/* =========================
   PROFILE
========================= */

function loadProfile() {

    const profileName  = document.getElementById("profileName")
    const profileEmail = document.getElementById("profileEmail")

    if (!profileName || !profileEmail) return

    profileName.innerText  = localStorage.getItem("username") || ""
    profileEmail.innerText = localStorage.getItem("email")    || ""
}

/* =========================
   CITY NAME
========================= */

async function loadCityName() {

    try {

        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&accept-language=en&lat=${userLocation.lat}&lon=${userLocation.lng}`

        const res  = await fetch(url)
        const data = await res.json()

        const city =
            data.address.city    ||
            data.address.town    ||
            data.address.village ||
            data.address.county  ||
            "Unknown"

        const header = document.getElementById("cityHeader")
        if (header) header.innerText = `🏥 MediFind - ${city}`

    } catch {
        console.log("City detection failed")
    }
}

/* =========================
   SWITCH ACCOUNT / LOGOUT
========================= */

function switchAccount() {
    localStorage.clear()
    window.location.replace("/")
}

function logout() {
    localStorage.clear()
    window.location.replace("/")
}

/* =========================
   RESET CHAT
========================= */

function resetChat() {

    symptomConversation = []
    followupStage       = 0
    pendingSymptom      = ""

    const chatBox = document.getElementById("chatBox")
    chatBox.innerHTML = ""

    appendBotText("Hello! Tell me your symptoms.")
}

/* =========================
   CHAT HELPERS

   Always use createElement() + appendChild() so that existing
   DOM nodes and their event-listeners are never destroyed.
========================= */

// Append a pre-built DOM node wrapped in a .bot bubble
function appendBotNode(node) {

    const chatBox = document.getElementById("chatBox")

    const wrapper = document.createElement("div")
    wrapper.className = "bot"
    wrapper.appendChild(node)

    chatBox.appendChild(wrapper)
    chatBox.scrollTop = chatBox.scrollHeight
}

// Append plain text / simple display HTML (no interactive buttons)
function appendBotText(html) {

    const chatBox = document.getElementById("chatBox")

    const wrapper = document.createElement("div")
    wrapper.className = "bot"
    wrapper.innerHTML = String(html || "").replace(/\n/g, "<br>")

    chatBox.appendChild(wrapper)
    chatBox.scrollTop = chatBox.scrollHeight
}

// Append a red emergency alert bubble
function appendEmergencyAlert(text) {

    const chatBox = document.getElementById("chatBox")

    const wrapper = document.createElement("div")
    wrapper.className = "bot emergency-alert"
    wrapper.innerHTML = String(text || "").replace(/\n/g, "<br>")

    chatBox.appendChild(wrapper)
    chatBox.scrollTop = chatBox.scrollHeight
}

// Append a user message
function addUser(text) {

    const chatBox = document.getElementById("chatBox")

    const div = document.createElement("div")
    div.className   = "user"
    div.textContent = text

    chatBox.appendChild(div)
    chatBox.scrollTop = chatBox.scrollHeight
}

/* =========================
   ENTER KEY
========================= */

function handleEnter(e) {
    if (e.key === "Enter") sendMessage()
}

/* =========================
   DIRECTIONS
========================= */

function openDirections(url) {
    window.open(url, "_blank")
}

/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    const input = document.getElementById("userInput")
    const text  = input.value.trim()

    if (!text) return

    addUser(text)
    input.value = ""

    // Show thinking indicator
    const chatBox     = document.getElementById("chatBox")
    const thinkingDiv = document.createElement("div")
    thinkingDiv.className = "bot"
    thinkingDiv.id        = "thinkingBot"
    thinkingDiv.innerHTML = "<div class='thinking'>Thinking...</div>"
    chatBox.appendChild(thinkingDiv)
    chatBox.scrollTop = chatBox.scrollHeight

    try {

        const res = await fetch(`${API}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symptom:        text,
                lat:            userLocation.lat,
                lng:            userLocation.lng,
                followup_stage: followupStage,
                conversation:   symptomConversation
            })
        })

        // Remove thinking indicator
        const oldThinking = document.getElementById("thinkingBot")
        if (oldThinking) oldThinking.remove()

        if (!res.ok) {
            appendBotText("Server connection error")
            return
        }

        let data = {}
        try {
            data = await res.json()
        } catch {
            appendBotText("Invalid server response")
            return
        }

        console.log("BACKEND RESPONSE:", data)

        // Always sync conversation from backend response
        if (data.conversation && Array.isArray(data.conversation)) {
            symptomConversation = data.conversation
        }

        // ── chat type ──
        if (data.type === "chat") {
            appendBotText(data.reply || data.message || "Hello!")
            return
        }

        // ── emergency ──
        if (data.type === "emergency") {
            appendEmergencyAlert(data.reply)
            symptomConversation = []
            followupStage       = 0
            pendingSymptom      = ""
            return
        }

        // ── followup question ──
        if (data.type === "followup_question" || data.type === "followup") {

            followupStage = typeof data.stage === "number" ? data.stage : followupStage + 1

            appendBotText(
                data.reply    ||
                data.question ||
                data.message  ||
                "Please provide more details."
            )
            return
        }

        // ── followup complete → show Recommend / No Thanks buttons ──
        if (data.type === "followup_complete" || data.type === "recommendation_ready") {

            followupStage = 0

            // Capture pendingSymptom AND doctor_type BEFORE clearing the conversation,
            // so getRecommendations() always has a non-empty query to send.
            pendingSymptom     = symptomConversation.join(" ") || text
            const doctorType   = data.doctor_type || ""

            symptomConversation = []

            const container = document.createElement("div")

            const p = document.createElement("p")
            p.textContent = data.reply || "I now have enough information."
            container.appendChild(p)

            const btnRow = document.createElement("div")
            btnRow.className = "recommend-buttons"

            const recommendBtn = document.createElement("button")
            recommendBtn.textContent = "Recommend Doctors"
            recommendBtn.addEventListener("click", () =>
                getRecommendations(pendingSymptom, doctorType)
            )

            const dismissBtn = document.createElement("button")
            dismissBtn.textContent = "No Thanks"
            dismissBtn.addEventListener("click", () => {
                btnRow.remove()
                const done = document.createElement("p")
                done.textContent = "Alright 👍"
                container.appendChild(done)
                symptomConversation = []
                followupStage       = 0
                pendingSymptom      = ""
            })

            btnRow.appendChild(recommendBtn)
            btnRow.appendChild(dismissBtn)
            container.appendChild(btnRow)

            appendBotNode(container)
            return
        }

        // ── direct doctor list ──
        if (data.doctors && Array.isArray(data.doctors)) {
            renderDoctors(data)
            return
        }

        // ── standard message ──
        if (data.message) {
            appendBotText(data.message)
            return
        }

        console.log("UNKNOWN RESPONSE:", data)
        appendBotText("Unable to process request")

    } catch (err) {

        console.error("FRONTEND ERROR:", err)

        const oldThinking = document.getElementById("thinkingBot")
        if (oldThinking) oldThinking.remove()

        appendBotText("Server connection error")
    }
}

/* =========================
   RECOMMENDATIONS
========================= */

async function getRecommendations(symptom, doctorType) {

    const query = symptom || pendingSymptom

    if (!query || query.trim() === "") {
        appendBotText("No symptom information found. Please describe your symptoms first.")
        return
    }

    appendBotText("Finding nearest doctors...")

    try {

        const body = {
            symptom: query,
            lat:     userLocation.lat,
            lng:     userLocation.lng
        }

        // If doctor_type is already known, send it so the backend skips
        // a redundant LLM call (avoids specialization mismatch on second call).
        if (doctorType) body.doctor_type = doctorType

        const res = await fetch(`${API}/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        })

        if (!res.ok) {
            appendBotText("Failed to fetch recommendations")
            return
        }

        const data = await res.json()
        console.log("RECOMMENDATION RESPONSE:", data)

        renderDoctors(data)

    } catch (err) {
        console.error("RECOMMEND ERROR:", err)
        appendBotText("Unable to fetch doctors")
    }
}

/* =========================
   RENDER DOCTORS
========================= */

function renderDoctors(data) {

    if (!data || !data.doctors || !Array.isArray(data.doctors)) {
        appendBotText("No doctors found")
        return
    }

    const container = document.createElement("div")

    const heading = document.createElement("h3")
    heading.textContent = `🩺 ${data.doctor_type || "Recommended Doctors"}`
    container.appendChild(heading)

    data.doctors.forEach(d => {

        const distance =
            d.distance !== undefined &&
            d.distance !== null &&
            d.distance < 9999
                ? Number(d.distance).toFixed(2) + " km"
                : "N/A"

        const card = document.createElement("div")
        card.className = "doctor-card" + (d.best ? " best" : "")

        const info = document.createElement("div")
        info.innerHTML = `
            ${d.best ? "<b>⭐ NEAREST DOCTOR</b><br><br>" : ""}
            <h3>${d.doctor    || "Unknown Doctor"}</h3>
            <p>🏥 ${d.hospital   || "Unknown Hospital"}</p>
            <p>📍 ${d.area       || "Unknown Area"}</p>
            <p>💉 ${d.speciality || "General"}</p>
            <p>⭐ ${d.rating     || "N/A"}</p>
            <p>📏 ${distance}</p>
        `
        card.appendChild(info)

        const btnRow = document.createElement("div")
        btnRow.className = "card-buttons"

        if (d.maps) {
            const dirBtn = document.createElement("button")
            dirBtn.textContent = "Directions"
            dirBtn.addEventListener("click", () => openDirections(d.maps))
            btnRow.appendChild(dirBtn)
        }

        const bookBtn = document.createElement("button")
        bookBtn.textContent = "Book"
        bookBtn.addEventListener("click", () => openBooking(d.doctor || "", d.hospital || ""))
        btnRow.appendChild(bookBtn)

        card.appendChild(btnRow)
        container.appendChild(card)
    })

    appendBotNode(container)

    // Reset state after displaying results
    symptomConversation = []
    followupStage       = 0
    pendingSymptom      = ""
}

/* =========================
   OPEN BOOKING
========================= */

async function openBooking(doctor, hospital) {

    currentDoctor   = doctor
    currentHospital = hospital

    document.getElementById("bookingModal").style.display = "flex"
    document.getElementById("bookingDoctor").innerText    = `${doctor} - ${hospital}`
    document.getElementById("appointmentDate").value      = ""

    loadSlots(doctor)
}

/* =========================
   CLOSE MODAL
========================= */

function closeModal() {
    document.getElementById("bookingModal").style.display = "none"
}

/* =========================
   LOAD SLOTS
========================= */

async function loadSlots(doctor) {

    const select = document.getElementById("slotSelect")
    select.innerHTML = `<option value="">Select Slot</option>`

    try {

        const res  = await fetch(`${API}/slots/${encodeURIComponent(doctor)}`)
        const data = await res.json()

        if (!data.slots || data.slots.length === 0) {
            const opt = document.createElement("option")
            opt.disabled    = true
            opt.textContent = "No slots available"
            select.appendChild(opt)
            return
        }

        data.slots.forEach(slot => {
            const opt = document.createElement("option")
            opt.value       = slot
            opt.textContent = slot
            select.appendChild(opt)
        })

    } catch {
        alert("Failed to load slots")
    }
}

/* =========================
   CONFIRM BOOKING
========================= */

async function confirmBooking() {

    const date = document.getElementById("appointmentDate").value
    const time = document.getElementById("slotSelect").value

    if (!date || !time) {
        alert("Select date and slot")
        return
    }

    // user_id must be an integer; localStorage always returns strings
    const userId = parseInt(localStorage.getItem("user_id"), 10)

    if (!userId) {
        alert("Not logged in. Please login again.")
        window.location.replace("/")
        return
    }

    try {

        const res = await fetch(`${API}/book`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id:     userId,
                doctor_name: currentDoctor,
                hospital:    currentHospital,
                date,
                time
            })
        })

        const data = await res.json()

        if (!res.ok) {
            alert(data.detail || "Booking failed")
            return
        }

        alert("Appointment booked successfully!")
        closeModal()
        loadAppointments()

    } catch {
        alert("Booking failed")
    }
}

/* =========================
   CANCEL APPOINTMENT
========================= */

async function cancelAppointment(id) {

    if (!confirm("Cancel this appointment?")) return

    try {

        const res  = await fetch(`${API}/cancel/${id}`, { method: "DELETE" })
        const data = await res.json()

        if (!res.ok) {
            alert(data.detail || "Cancellation failed")
            return
        }

        alert("Appointment cancelled")
        loadAppointments()

    } catch {
        alert("Cancellation failed")
    }
}

/* =========================
   LOAD APPOINTMENTS
========================= */

async function loadAppointments() {

    const upcoming = document.getElementById("upcomingAppointments")
    const previous = document.getElementById("previousAppointments")

    if (!upcoming || !previous) return

    upcoming.innerHTML = ""
    previous.innerHTML = ""

    const userId = localStorage.getItem("user_id")
    if (!userId) return

    try {

        const res  = await fetch(`${API}/appointments/${userId}`)
        const data = await res.json()

        const makeCard = (a, showCancel) => {

            const card = document.createElement("div")
            card.className = "appointment-card"

            const info = document.createElement("div")
            info.innerHTML = `
                <h4>${a.doctor}</h4>
                <p>💉 ${a.speciality || ""}</p>
                <p>🏥 ${a.hospital}</p>
                <p>📍 ${a.city || ""}</p>
                <p>📅 ${a.date}</p>
                <p>⏰ ${a.time}</p>
            `
            card.appendChild(info)

            if (showCancel) {

                const btnRow = document.createElement("div")
                btnRow.className = "card-buttons"

                if (a.maps) {
                    const dirBtn = document.createElement("button")
                    dirBtn.textContent = "Directions"
                    dirBtn.addEventListener("click", () => openDirections(a.maps))
                    btnRow.appendChild(dirBtn)
                }

                const cancelBtn = document.createElement("button")
                cancelBtn.textContent = "Cancel"
                cancelBtn.addEventListener("click", () => cancelAppointment(a.id))
                btnRow.appendChild(cancelBtn)

                card.appendChild(btnRow)
            }

            return card
        }

        if (data.upcoming.length === 0) {
            const p = document.createElement("p")
            p.style.color = "#888"
            p.textContent = "No upcoming appointments"
            upcoming.appendChild(p)
        } else {
            data.upcoming.forEach(a => upcoming.appendChild(makeCard(a, true)))
        }

        if (data.previous.length === 0) {
            const p = document.createElement("p")
            p.style.color = "#888"
            p.textContent = "No previous appointments"
            previous.appendChild(p)
        } else {
            data.previous.forEach(a => previous.appendChild(makeCard(a, false)))
        }

    } catch {
        console.log("Appointments failed")
    }
}

/* =========================
   WINDOW LOAD
========================= */

window.onload = () => {

    // Index / auth page
    if (document.getElementById("signupBox")) {
        showLogin()
        return
    }

    // Chat page — redirect to login if no session
    const userId = localStorage.getItem("user_id")

    if (!userId) {
        window.location.replace("/")
        return
    }

    loadProfile()
    loadAppointments()
}

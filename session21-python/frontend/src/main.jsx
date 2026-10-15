import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
const API = "/api";
function App() {
  const [tasks, setTasks] = useState([]),
    [stats, setStats] = useState({ total: 0, todo: 0, inProgress: 0, done: 0 }),
    [filter, setFilter] = useState("ALL"),
    [showForm, setShowForm] = useState(false),
    [loading, setLoading] = useState(true),
    [error, setError] = useState("");
  const load = async () => {
    try {
      setError("");
      const [a, b] = await Promise.all([
        fetch(`${API}/tasks`),
        fetch(`${API}/tasks/stats`),
      ]);
      if (!a.ok || !b.ok) throw Error("Backend unavailable");
      setTasks(await a.json());
      setStats(await b.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    load();
  }, []);
  const visible =
    filter === "ALL" ? tasks : tasks.filter((t) => t.status === filter);
  const update = async (t) => {
    try {
      setError("");
      const next =
        t.status === "TODO"
          ? "IN_PROGRESS"
          : t.status === "IN_PROGRESS"
            ? "DONE"
            : "TODO";
      const response = await fetch(`${API}/tasks/${t.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: next }),
      });
      if (!response.ok) throw Error("Could not update the assignment");
      await load();
    } catch (e) {
      setError(e.message);
    }
  };
  const create = async (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    const f = new FormData(form);
    try {
      setError("");
      const response = await fetch(`${API}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: f.get("title"),
          description: f.get("description"),
          priority: f.get("priority"),
          assignee: f.get("assignee"),
          session_number: f.get("session_number")
            ? Number(f.get("session_number"))
            : null,
          due_date: f.get("due_date") || null,
          status: "TODO",
        }),
      });
      if (!response.ok)
        throw Error(
          "Could not save the assignment. Check the form and try again.",
        );
      form.reset();
      setShowForm(false);
      await load();
    } catch (e) {
      setError(e.message);
    }
  };
  const remove = async (t) => {
    try {
      setError("");
      const response = await fetch(`${API}/tasks/${t.id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw Error("Could not delete the assignment");
      await load();
    } catch (e) {
      setError(e.message);
    }
  };
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">T</span>
          <div>
            <b>Homework Tracker</b>
            <small>Coursework</small>
          </div>
        </div>
        <nav>
          <span className="active">▦ Dashboard</span>
        </nav>
        <div className="side-bottom">
          <div className="upgrade">
            <strong>Session by session.</strong>
            <p>Keep assignments, test output and screenshots together.</p>
          </div>
          <div className="profile">
            <div className="avatar">KJ</div>
            <div>
              <b>Kartik</b>
              <small>Developer</small>
            </div>
            <span>⋮</span>
          </div>
        </div>
      </aside>
      <main className="main">
        <header>
          <div>
            <p className="eyebrow">COURSE / ASSIGNMENTS</p>
            <h1>Course assignments</h1>
            <p className="muted">Track each session’s assignment.</p>
          </div>
          <button className="primary" onClick={() => setShowForm(true)}>
            ＋ New assignment
          </button>
        </header>
        {error && (
          <div className="alert" role="alert">
            ⚠ {error}. Check the connection and try again.
          </div>
        )}
        <section className="stats">
          <Stat label="Total tasks" value={stats.total} icon="▦" />
          <Stat label="To do" value={stats.todo} icon="○" />
          <Stat label="In progress" value={stats.inProgress} icon="◔" />
          <Stat label="Completed" value={stats.done} icon="✓" />
        </section>
        <section className="content-grid">
          <div className="panel tasks-panel">
            <div className="panel-head">
              <div>
                <h2>Tasks</h2>
                <p className="muted">Assignments and their current status.</p>
              </div>
              <div className="filters">
                {["ALL", "TODO", "IN_PROGRESS", "DONE"].map((x) => (
                  <button
                    className={filter === x ? "selected" : ""}
                    onClick={() => setFilter(x)}
                    key={x}
                  >
                    {x === "ALL" ? "All" : x.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>
            {loading ? (
              <div className="empty">Loading tasks…</div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Task</th>
                      <th>Assignee</th>
                      <th>Priority</th>
                      <th>Status</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {visible.map((t) => (
                      <tr key={t.id}>
                        <td>
                          <div className="task-title">
                            <span
                              className={`dot ${t.status.toLowerCase()}`}
                            ></span>
                            <div>
                              <b>{t.title}</b>
                              <small>{t.description}</small>
                              <small>
                                {t.session_number
                                  ? `Session ${t.session_number}`
                                  : "No session"}
                                {t.due_date ? ` · Due ${t.due_date}` : ""}
                              </small>
                            </div>
                          </div>
                        </td>
                        <td>{t.assignee}</td>
                        <td>
                          <span
                            className={`priority ${t.priority.toLowerCase()}`}
                          >
                            {t.priority}
                          </span>
                        </td>
                        <td>
                          <span className={`status ${t.status.toLowerCase()}`}>
                            {t.status.replace("_", " ")}
                          </span>
                        </td>
                        <td>
                          <button
                            className="icon-btn"
                            onClick={() => update(t)}
                            title="Advance status"
                          >
                            ↻
                          </button>{" "}
                          <button
                            className="icon-btn"
                            onClick={() => remove(t)}
                            title="Delete assignment"
                          >
                            ×
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!visible.length && (
                  <div className="empty">No tasks in this filter.</div>
                )}
              </div>
            )}
          </div>
          <aside className="panel activity">
            <div className="panel-head">
              <div>
                <h2>Submission checklist</h2>
                <p className="muted">
                  Before sending homework to the instructor.
                </p>
              </div>
            </div>
            <Activity
              icon="1"
              text="Run and test the application"
              time="Keep the command output"
            />
            <Activity
              icon="2"
              text="Check the README and screenshots"
              time="Use relative image paths"
            />
            <Activity
              icon="3"
              text="Commit and push the session files"
              time="Submit the GitHub README link"
            />
          </aside>
        </section>
        {showForm && (
          <div className="modal-backdrop">
            <form className="modal" onSubmit={create}>
              {error && <p role="alert">{error}</p>}
              <div className="modal-head">
                <div>
                  <p className="eyebrow">NEW ASSIGNMENT</p>
                  <h2>Add an assignment</h2>
                </div>
                <button
                  type="button"
                  className="close"
                  onClick={() => setShowForm(false)}
                >
                  ×
                </button>
              </div>
              <label>
                Assignment title
                <input
                  name="title"
                  required
                  maxLength={200}
                  placeholder="e.g. Session 21 capstone"
                />
              </label>
              <div className="form-row">
                <label>
                  Course session
                  <input
                    name="session_number"
                    type="number"
                    min="1"
                    max="21"
                    defaultValue="21"
                  />
                </label>
                <label>
                  Due date
                  <input name="due_date" type="date" />
                </label>
              </div>
              <label>
                Description
                <textarea
                  name="description"
                  placeholder="What needs to be done?"
                />
              </label>
              <div className="form-row">
                <label>
                  Priority
                  <select name="priority">
                    <option>LOW</option>
                    <option>MEDIUM</option>
                    <option>HIGH</option>
                  </select>
                </label>
                <label>
                  Assignee
                  <input
                    name="assignee"
                    maxLength={120}
                    defaultValue="Kartik"
                  />
                </label>
              </div>
              <button className="primary full">Save assignment</button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
function Stat({ label, value, icon }) {
  return (
    <div className="stat">
      <div className="stat-icon">{icon}</div>
      <div>
        <small>{label}</small>
        <strong>{value}</strong>
        <span>Updated just now</span>
      </div>
    </div>
  );
}
function Activity({ icon, text, time }) {
  return (
    <div className="activity-row">
      <span className="activity-icon">{icon}</span>
      <div>
        <b>{text}</b>
        <small>{time}</small>
      </div>
    </div>
  );
}
createRoot(document.getElementById("root")).render(<App />);

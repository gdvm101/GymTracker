import StatusPage from "../pages/StatusPage.jsx";

export default function App() {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="container topbar-inner">
          <a className="brand" href="/" aria-label="GymTracker, главная">
            <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
            GymTracker
          </a>
          <span className="product">Дневник силовых тренировок</span>
        </div>
      </header>
      <StatusPage />
      <footer className="container footer">Учебный проект ПетрГУ</footer>
    </div>
  );
}

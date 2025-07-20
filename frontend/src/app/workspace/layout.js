import TopNav from "@/components/TopNav/TopNav";
import "./workspace.scss";

export default function Layout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="work-space-wrap">
          <TopNav />
          <main className="workspace-body">{children}</main>
        </div>
      </body>
    </html>
  );
}

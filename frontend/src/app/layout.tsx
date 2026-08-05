export const dynamic = "force-dynamic";
export const dynamic = "force-dynamic";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UDIAP — Universal Decision Intelligence Assessment Platform",
  description:
    "Measure How Humans Think, Decide and Adapt. AI-powered cognitive decision intelligence platform.",
  keywords: ["AI", "Decision Intelligence", "Cognitive Computing", "Assessment"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-udiap-bg text-slate-100">
        {children}
      </body>
    </html>
  );
}

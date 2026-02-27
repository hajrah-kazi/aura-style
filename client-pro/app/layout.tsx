import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "AuraStyle | Intelligent Recommendations",
    description: "Next-gen E-commerce Recommendation Engine",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <div className="flex flex-col min-h-screen">
                    <main className="flex-grow">{children}</main>
                </div>
            </body>
        </html>
    );
}

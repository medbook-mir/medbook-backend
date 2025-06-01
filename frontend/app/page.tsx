// Import your Client Component
import HomePage from "./home";

// async function getPosts() {
//   const res = await fetch('https://...')
//   const posts = await res.json()
//   return posts
// }

export default async function Page({}) {
  //   const recentPosts = await getPosts()

  return <HomePage />;
}

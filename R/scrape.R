library(tabulizer)

scrape_pdf_urls <- function(pdf_urls, file) {
  content <- c()
  for (url in pdf_urls) {
    text <- extract_text(url)
    content <- c(content, strsplit(gsub("\n", " ", text), " "))
  }
  content <- unlist(content)
}

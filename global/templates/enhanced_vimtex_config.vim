" Enhanced VimTeX Configuration for Beautiful LaTeX Notes
" Based on Gilles Castel's approach with NotesTeX aesthetics

" Check if required plugins are available
let s:has_vimtex = exists('g:vimtex_enabled') || exists('*vimtex#init')
let s:has_ultisnips = exists('g:UltiSnipsExpandTrigger')

if !s:has_vimtex
    echo "Warning: VimTeX plugin not found. Please install it with your plugin manager."
    echo "For vim-plug, add: Plug 'lervag/vimtex'"
endif

if !s:has_ultisnips
    echo "Warning: UltiSnips plugin not found. Please install it with your plugin manager."
    echo "For vim-plug, add: Plug 'SirVer/ultisnips'"
endif

" VimTeX configuration
let g:tex_flavor='latex'
let g:vimtex_view_method='zathura'
let g:vimtex_quickfix_mode=0
let g:vimtex_compiler_latexmk = {
    \ 'build_dir' : '',
    \ 'callback' : 1,
    \ 'continuous' : 1,
    \ 'executable' : 'latexmk',
    \ 'hooks' : [],
    \ 'options' : [
    \   '-verbose',
    \   '-file-line-error',
    \   '-synctex=1',
    \   '-interaction=nonstopmode',
    \   '-shell-escape',
    \ ],
    \}

" Concealment for cleaner view
set conceallevel=2
let g:tex_conceal='abdmg'

" UltiSnips configuration (only if plugin is available)
if s:has_ultisnips
    let g:UltiSnipsExpandTrigger = '<tab>'
    let g:UltiSnipsJumpForwardTrigger = '<tab>'
    let g:UltiSnipsJumpBackwardTrigger = '<s-tab>'
    let g:UltiSnipsSnippetDirectories = ['UltiSnips', '~/.vim/UltiSnips']
endif

" Spell checking disabled by default
" Uncomment the lines below if you want spell checking:
" setlocal spell
" set spelllang=en_us
" inoremap <C-l> <c-g>u<Esc>[s1z=`]a<c-g>u

" Enhanced LaTeX-specific keybindings
augroup LaTeX
    autocmd!
    autocmd FileType tex inoremap <buffer> ,, \,
    autocmd FileType tex inoremap <buffer> ;; \;
    autocmd FileType tex inoremap <buffer> jk <Esc>
    
    " Quick compilation and view
    autocmd FileType tex nnoremap <buffer> <leader>ll :VimtexCompile<CR>
    autocmd FileType tex nnoremap <buffer> <leader>lv :VimtexView<CR>
    autocmd FileType tex nnoremap <buffer> <leader>lc :VimtexClean<CR>
    autocmd FileType tex nnoremap <buffer> <leader>le :VimtexErrors<CR>
    autocmd FileType tex nnoremap <buffer> <leader>ls :VimtexStatus<CR>
    autocmd FileType tex nnoremap <buffer> <leader>lt :VimtexTocToggle<CR>
    
    " Research-specific shortcuts
    autocmd FileType tex nnoremap <buffer> <leader>nn :call CreateTodayNote()<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sn :call InsertSidenote()<CR>
    autocmd FileType tex nnoremap <buffer> <leader>mn :call InsertMarginNote()<CR>
    autocmd FileType tex nnoremap <buffer> <leader>td :call InsertTodo()<CR>
    autocmd FileType tex nnoremap <buffer> <leader>id :call InsertIdea()<CR>
    autocmd FileType tex nnoremap <buffer> <leader>hl :call InsertHighlight()<CR>
    
    " Section editing shortcuts
    autocmd FileType tex nnoremap <buffer> <leader>si :call EditSection('introduction')<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sm :call EditSection('methods')<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sr :call EditSection('results')<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sd :call EditSection('discussion')<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sc :call EditSection('conclusion')<CR>
    autocmd FileType tex nnoremap <buffer> <leader>sb :call EditBibliography()<CR>
augroup END

" Function to create today's note (with better error handling)
function! CreateTodayNote()
    let today = strftime("%Y-%m-%d")
    let note_file = "notes/note-" . today . ".tex"
    
    " Create notes directory if it doesn't exist
    if !isdirectory("notes")
        call mkdir("notes", "p")
    endif
    
    if filereadable(note_file)
        execute "edit " . note_file
    else
        " Create a simple note template instead of relying on external script
        let template_content = [
            \ "% Note for " . today,
            \ "\\documentclass{article}",
            \ "\\usepackage[utf8]{inputenc}",
            \ "\\title{Notes - " . today . "}",
            \ "\\author{Research Notes}",
            \ "\\date{" . today . "}",
            \ "",
            \ "\\begin{document}",
            \ "\\maketitle",
            \ "",
            \ "% Your notes here",
            \ "",
            \ "\\end{document}"
            \ ]
        call writefile(template_content, note_file)
        execute "edit " . note_file
        echo "Created new note: " . note_file
    endif
endfunction

" Function to insert sidenote
function! InsertSidenote()
    let text = input("Sidenote text: ")
    if text != ""
        execute "normal! a\\sn{" . text . "}"
    endif
endfunction

" Function to insert margin note
function! InsertMarginNote()
    let text = input("Margin note text: ")
    if text != ""
        execute "normal! a\\mn{" . text . "}"
    endif
endfunction

" Function to insert todo
function! InsertTodo()
    let text = input("Todo text: ")
    if text != ""
        execute "normal! a\\todo{" . text . "}"
    endif
endfunction

" Function to insert idea
function! InsertIdea()
    let text = input("Idea text: ")
    if text != ""
        execute "normal! a\\idea{" . text . "}"
    endif
endfunction

" Function to insert highlight
function! InsertHighlight()
    let text = input("Highlight text: ")
    if text != ""
        execute "normal! a\\highlight{" . text . "}"
    endif
endfunction

" Function to edit sections (with better error handling)
function! EditSection(section)
    let section_file = "sections/" . a:section . ".tex"
    
    " Create sections directory if it doesn't exist
    if !isdirectory("sections")
        call mkdir("sections", "p")
    endif
    
    if filereadable(section_file)
        execute "edit " . section_file
    else
        " Create a simple section template
        let template_content = [
            \ "% " . toupper(a:section) . " section",
            \ "\\section{" . toupper(a:section[0]) . a:section[1:] . "}",
            \ "",
            \ "% Content for " . a:section . " section goes here",
            \ ""
            \ ]
        call writefile(template_content, section_file)
        execute "edit " . section_file
        echo "Created new section: " . section_file
    endif
endfunction

" Function to edit bibliography (with better error handling)
function! EditBibliography()
    let bib_files = ["references.bib", "bibliography.bib", "refs.bib"]
    let found = 0
    
    for bib_file in bib_files
        if filereadable(bib_file)
            execute "edit " . bib_file
            let found = 1
            break
        endif
    endfor
    
    if !found
        " Create a new bibliography file
        let new_bib = "references.bib"
        let template_content = [
            \ "% Bibliography file",
            \ "% Add your references here",
            \ "",
            \ "% Example entry:",
            \ "% @article{author2023,",
            \ "%   author = {Author Name},",
            \ "%   title = {Article Title},",
            \ "%   journal = {Journal Name},",
            \ "%   year = {2023},",
            \ "%   volume = {1},",
            \ "%   pages = {1--10}",
            \ "% }",
            \ ""
            \ ]
        call writefile(template_content, new_bib)
        execute "edit " . new_bib
        echo "Created new bibliography: " . new_bib
    endif
endfunction

" Enhanced syntax highlighting for research notes
augroup ResearchNotes
    autocmd!
    autocmd FileType tex syntax match researchTodo /\\todo{[^}]*}/
    autocmd FileType tex syntax match researchIdea /\\idea{[^}]*}/
    autocmd FileType tex syntax match researchHighlight /\\highlight{[^}]*}/
    autocmd FileType tex syntax match researchSidenote /\\sn{[^}]*}/
    autocmd FileType tex syntax match researchImportant /\\important{[^}]*}/
    
    autocmd FileType tex highlight researchTodo ctermfg=yellow guifg=orange
    autocmd FileType tex highlight researchIdea ctermfg=green guifg=lightgreen
    autocmd FileType tex highlight researchHighlight ctermfg=blue guifg=lightblue
    autocmd FileType tex highlight researchSidenote ctermfg=gray guifg=gray
    autocmd FileType tex highlight researchImportant ctermfg=red guifg=red
augroup END

" Auto-completion for research commands
augroup ResearchCompletion
    autocmd!
    autocmd FileType tex setlocal omnifunc=ResearchComplete
augroup END

function! ResearchComplete(findstart, base)
    if a:findstart
        let line = getline('.')
        let start = col('.') - 1
        while start > 0 && line[start - 1] =~ '\a'
            let start -= 1
        endwhile
        return start
    else
        let completions = []
        let research_commands = ['todo', 'idea', 'highlight', 'sn', 'mn', 'important', 'reading']
        
        for cmd in research_commands
            if cmd =~ '^' . a:base
                call add(completions, cmd)
            endif
        endfor
        
        return completions
    endif
endfunction

" Enhanced fold settings for better organization
augroup LatexFolding
    autocmd!
    autocmd FileType tex setlocal foldmethod=expr
    autocmd FileType tex setlocal foldexpr=LatexFoldExpr(v:lnum)
    autocmd FileType tex setlocal foldtext=LatexFoldText()
augroup END

function! LatexFoldExpr(lnum)
    let line = getline(a:lnum)
    if line =~ '\\section{'
        return '>1'
    elseif line =~ '\\subsection{'
        return '>2'
    elseif line =~ '\\subsubsection{'
        return '>3'
    elseif line =~ '\\begin{progress}'
        return '>1'
    elseif line =~ '\\begin{ideas}'
        return '>1'
    elseif line =~ '\\begin{questions}'
        return '>1'
    elseif line =~ '\\begin{references}'
        return '>1'
    elseif line =~ '\\begin{notes}'
        return '>1'
    else
        return '='
    endif
endfunction

function! LatexFoldText()
    let line = getline(v:foldstart)
    let line = substitute(line, '^\s*', '', '')
    let line = substitute(line, '{.*}', '', '')
    return line . ' (' . (v:foldend - v:foldstart + 1) . ' lines)'
endfunction

echo "Enhanced VimTeX configuration loaded for beautiful LaTeX notes!"
echo "Requirements:"
echo "  - VimTeX plugin: Plug 'lervag/vimtex'"
echo "  - UltiSnips plugin: Plug 'SirVer/ultisnips'"
echo "  - Zathura PDF viewer (for viewing PDFs)"
echo ""
echo "Key mappings:"
echo "  <leader>ll  - Compile"
echo "  <leader>lv  - View PDF"
echo "  <leader>lc  - Clean"
echo "  <leader>le  - Show errors"
echo "  <leader>nn  - Create/open today's note"
echo "  <leader>sn  - Insert sidenote"
echo "  <leader>mn  - Insert margin note"
echo "  <leader>td  - Insert todo"
echo "  <leader>id  - Insert idea"
echo "  <leader>hl  - Insert highlight"
echo "  <leader>si  - Edit introduction"
echo "  <leader>sm  - Edit methods"
echo "  <leader>sr  - Edit results"
echo "  <leader>sd  - Edit discussion"
echo "  <leader>sc  - Edit conclusion"
echo "  <leader>sb  - Edit bibliography"

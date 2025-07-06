1. Basic Product 
    - ~~Get the frontend ready for file uplaod and display it ~~--- D 

    1.2. ~~Send pdf to backend, by selecting either ppt or audio button, so pass the flag var with the file~~ --- D 
    - ~~remove the file-id, the in-memory work-around for database storage --- do later, first do 1.3,~~ 
    - Execute the graph flow accordingly
    - improve the routes for audio : why convo and summary separate? wont make sense after splitting graph with conditional edge

    1.3. ~~Send results to frontend~~
    - ~~First deal with sending ppt, then somehow display it, maybe using iframe~~ _can't display, only download ppt_
    - ~~For podcast, just combine entire audio to single mp3 file, with the default iframe media player~~ 
    - ~~Give download option for both~~ 

    1.4. Setup authentication
    - Google or email, whichever is easier, login stuff with firebase backend

    1.5. Smooth Operation  
    - Ensure both functionalites run properly with LLM calls   
    
    1.6. Guardrails
    - handle the case if pdf is not res paper, and so that I dont get 500 error due to nonetype
    - like add a guardrail node where, a cheaper llm perhaps, check if uploaded pdf is res paper or not

2. Improvement
    - Account related Improvement  
        - Store the graph state for a particular pdf
        - when generating either ppt or audio, check if extract text already available
        - when asking for either again, check if it already exists, then serve that

    - Content Improvements:
        -  enhance the prompts, for podcast, to generate more engaging stuff, 
        not include the whole author name, avoid spelling stuff like "company name Trademark"
        - introduce somebackground of the topic of the paper
        and do some meta-prompting
        - for ppt, try out the prompts from the notebook and ofc meta-prompting
    - Think about async functions

    - Becuase we're storing graph states, show a page of "My PPTs" and "My Podcasts"

3. Customizations
    - Explore other than pptx options for generating ppt, like md based and other css embeded stuff and different prompts as in the notebook
    - Fancier podcast playback, with two speaker waves animation
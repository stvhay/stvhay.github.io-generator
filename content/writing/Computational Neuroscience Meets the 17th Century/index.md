+++
date = '2025-05-27T15:48:07-04:00'
draft = false
title = 'Computational Neuroscience Meets the 17th Century'
+++
*Do we live in a world of ideas?* :bulb:
<!--more-->

Descartes famously kicked off an era of Western philosophy with his famous statement "Cogito, ergo sum" (I think, therefore I am). He went on to develop a dualistic theory of mind and body. The theory posits that the world is composed of fundamentally two types of 'stuff': stuff that extends into the three-dimensional space (matter) and suff that doesnt (ideas). For a long time this idea was popular, but in modern circles of philosophy, it has largely gone out of fashion in favor of materialism, which seems more sensible nowadays where technology and science so fundamentally shape our worldview.

In the 17th century, things weren't quite as settled. Irish philosopher George Berkeley believed the opposite of materialism&mdash;the world (including all matter) was composed only of ideas [^1]. Like materialists, he didn't really understand how dualism could make much sense (how does spirit interact with matter exactly?). My question is: **does idealism offer us any relevant perspective when we study neuroscience**?

A 2014 paper[^2] summarized the current state of neuroscience research on scene analysis&mdash;the study of how our brain turns converts sense-data into an internal representation of the world we see around us. It then argued that scene analysis is not only an incredibly hard problem, but that many of the ways we study this problem fail to address very fundamental and obvious questions.

It turns out that most empirical research into scene analysis is conducted using very simplified forms&mdash;lines and basic geometric figures on simple backgrounds and neutral lighting. Arguably, this makes sense because it provides a controlled experimental environment. Unfortunately, while this research framework has given us many useful insights, we remain relatively stuck on how we map those insights to ecologically relevant scene analysis problems that all animals are constantly solving.[^4]

As I was reading, I was thinking about Berkeley's idealism. As I learn more about human perception, the more I realize that our perceptual world is far more like a Star Trek holodeck&mdash;_a constructed reality_&mdash;than an objective and independent interpretation of sense-data. Our lived experience is deeply subjective. Not only is our brain is deeply involved at every point in sensory processing, it constructs a model of the world from a surprisingly tiny subset of the information one might think is available. So, while I don't think the world is *literally* built of ideas, it is not a totally unreasonable way to approach how we study perception.

As an example, saccades are rapid eye movements that constantly shift our gaze. The movements are essential for our ability to process visual information because we physically don't have the bandwidth to take in all of our visual field in without some form of multiplexing[^3]. Our brain controls where our eyes are pointed based on a mix of unconscious neural control systems tracking our head, body, and eye position; random saccade and even smaller microsaccade movements, as well as high-level task-driven signals that determine our attention. All of the high-acuity visual data we get (e.g. detail and color) comes via a surprisingly narrow field of view, and the rest we fill in with prior knowledge and expectations and much more limited peripheral visual data.

This motif recurs throughout the perceptive systems of most animals. For example, the paper discusses jumping spiders that have three pairs of different kinds of eyes&mdash;only one of the pairs providing detail, and provides it as a one-dimensional vertical slit. The spider uses these eyes to scan selected areas of its visual field horizontally like a crazed dot-matrix [printer](https://youtu.be/A_vXA058EDY?t=23). Like us, the spider then assembles these samples into a three-dimensional representation of the world&mdash;the only way to explain its complex behaviors.

Bats have even more impressive autonomic systems in place to operate their neural sonar. Not only do they generate (encode) and process (decode) various sophisticated sonar signals, they focus sonic energy at targets of interest, and also actively adjust their sonar transmission frequencies away from those of nearby bats to reduce interference.

Meanwhile, some of our most famous computational models of vision bear little resemblance to these attention-driven biological systems. Consider the incredibly successful ResNet image classifier. It reads entire images, breaks them down into spatio-temporal chunks, then pieces it all back together into increasingly complex groups of pixels for grouping and labeling. While there is evidence for biological neurons doing spatio-temporal filtering[^5], Resnet has no concept of three-dimensional space other than what it has memorized, no opinions on what it should be paying attention to, and its overall computational structure doesn't have obvious traceability back to any biological systems. The success of ResNet has much more to do with its accomplishments as a technology than how it can explain the function of biological neural systems or animal behavior[^6].

Yet we have the urge to apply ResNet to our search to understand the biological brain because of its impressive performance and because it resonates with our lived experience of perception. The human vision system makes us feel very connected to the world. It feels like our eyes are like cameras taking pictures or video. Therefore, it seems like the mind might process images like ResNet. The unconscious mechanisms of eye movement could seem like boring biological engineering details&mdash;a distraction from the really interesting stuff that makes up human perception and thought.

So while we are not literally living in Berkeleyan world of ideas, the vast bulk of our perceptive reality can be viewed as a Berkeleyan mental construct. Our brain has made ourselves a holodeck[^8]. Disbanding our own internal percetual biases first leaves us with even more mysteries. However, a major thrust of this scene analysis paper is that we really should accept that and more closely examine mechanisms of animal perception to inform our hypotheses. Doing so puts direct scientific observation in the driver's seat, and gives us a more unbiased view into the functioning of our minds.

[^1]: Star Trek (TNG) not-so-famously introduced a character "Barclay" who was obsessed with spending time in the holodeck&mdash;a ship system that could create rich virtual environments. The character name might be a subtle nod to Berkeley or just a coincidence.

[^2]: Lewicki MS, Olshausen BA, Surlykke AS, and Moss CF. (2014) Scene analysis in the natural environment. _Frontiers in Psychology_ 199 doi:[10.3389/fpsycg.2014.00199](https://doi.org/10.3389/fpsyg.2014.00199)

[^3]: Saccades also compensate for our eyes being a kind of high pass filter, suppressing visual signals that aren't moving.

[^4]: Granted, it _has_ been a bit over 10 years since this paper was published... :joy:

[^5]: This is really just one of many papers: Field D. J. (1987). Relations between the statistics of natural images and the response properties of cortical cells. _J Opt Soc Am A., Optics and image science_, 4(12), 2379–2394. doi:[10.1364/josaa.4.002379](https://doi.org/10.1364/josaa.4.002379)

[^6]: There is a really intersting paper[^7] that attempts to do this with a pretty famous Google-developed neural network that broke Internet CAPTCHAs that I am probably going to write about soon.

[^7]: George D, Lázaro-Gredilla M, Lehrach W, Dedieu A, Zhou G, and Marino J. (2025) A detailed theory of thalamic and cortical microcircuits for predictive visual inference. _Sci. Adv._ 11, eadr6698. doi:[10.1126/sciadv.adr6698](https://doi.org/10.1126/sciadv.adr6698)

[^8]: See Footnote 1.

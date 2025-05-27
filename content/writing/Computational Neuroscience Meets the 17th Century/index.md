+++
date = '2025-05-27T15:48:07-04:00'
draft = false
title = 'Computational Neuroscience Meets the 17th Century'
+++
Descartes famously kicked off an era of Western philosophy with his famous statement "Cogito, ergo sum" (I think, therefore I am). He went on to develop a dualistic theory of mind and body. The theory posits that the world is composed of fundamentally two types of 'stuff': spirit and matter--and that these two types of stuff interact with each other. For a long time, most bought into this idea, but in modern circles of philosophy, it has largely gone out of fashion in favor of materialism (in various forms).

In the 17th century, things weren't quite as settled. Irish philosopher George Berkeley believed the opposite of materialism--the world (including all matter) was composed only of ideas [^1]. Like materialists, he didn't really understand how dualism could make much sense (how does spirit interact with matter exactly?). My question is: **does idealism offer us any relevant perspective when we study neuroscience**?

A 2014 [paper][2] summarized the current state of neuroscience research on scene analysis--the study of how our brain turns converts sense-data into an internal representation of the world we see around us. It then argued that scene analysis is not only an incredibly hard problem, but much of our study of this problem fails to address very fundamental and obvious questions.

It turns out that most scene analysis research is conducted with very simplified forms--lines and basic geometric figures. Arguably, this makes sense because it provides a controlled experimental environment. Unfortunately, while the research has given us many useful insights, we remain stuck on how we take this simplified experiment and map it to ecologically relevant scene analysis problems that all animals are constantly solving.

As I was reading, I was thinking about Berkeley's idealism. As I learn more about human perception, more evidence is presented that our perceptual world is far more like a Star Trek holodeck--a constructed reality--than an objective projection of sense-data. Not only is our brain is deeply involved at every point in this process, it constructs perception from a surprisingly tiny subset of the information we perceive. So, while I don't literally think the world is **literally** built of ideas, it is not a totally unreasonable way to approach how we study perception.

As an example, saccades are rapid eye movements that constantly shift our gaze. The movements are essential for our ability to process visual information because we simply don't have the bandwidth to take all of our visual field in without some form of multiplexing[^3]. Our brain controls where our eyes are pointed based on a mix of unconscious neural control systems tracking our head, body, and eye position; random **saccade** and **microsaccade** movement, as well as high-level task-driven signals that determine our attention. All of the high-acuity visual data we get (e.g. detail and color) comes via this narrow field of view, and the rest we fill in with prior knowledge and expectations and much more limited peripheral visual data.

This motif recurs throughout the animal kindgom. The scene analysis paper discusses jumping spiders that have three pairs of different kinds of eyes--only one pair providing detail, and doing so on a narrow vertical dimension. The spider uses these eyes to scan its visual field horizontally like a crazed dot-matrix [printer](https://youtu.be/A_vXA058EDY?t=23). Like us, the spider then assembles these samples into a three-dimensional representation of the world--the only way to explain its complex behaviors.

Bats have even more impressive autonomic systems in place to operate their neural sonar. Not only do they generate (encode) and process (decode) various aural sonar signals, they focus these waves at targets of interest, and adjust sonar transmission frequencies away from those of nearby bats.

Meanwhile, some of our most famous computational models of vision bear little resemblance to these attention-driven biological systems. For example, ResNet takes entire images, breaks them down into spatio-frequency chunks, then pieces it all back together into increasingly complex groups of pixels for grouping and labeling. Resnet has no concept of three-dimensional space other than what it has memorized, no opinions on whether it should or should not be paying attention to the things it identifies, and its computational structure doesn't have obvious traceability back to biological systems. The success of ResNet has much more to do with its accomplishments as a technology than how it can explain the function of biological neural systems or animal behavior.

Yet we have the urge to apply ResNet to our search to understand the biological brain because of its impressive performance and because it resonates with our lived experience of perception. The human vision system makes us feel very connected to the world. It feels like our eyes are like cameras taking pictures or video. Therefore, it seems like the mind might process images like ResNet. The unconscious mechanisms of eye movement could seem like boring biological engineering details--a distraction from the really interesting stuff that makes up human perception and thought.

So while we are not literally living in Berkeleyan world of ideas, the vast bulk of our perceptive reality can be viewed as a Berkeleyan mental construct. Our brain has made ourselves a holodeck[^1]. Disbanding our own percetual ideas about how our mind works leaves us with an even larger mystery. A major point of this scene analysis paper is that we really should accept that and more closely examine the mechanisms of animal perception to inform the direction of research. Doing so puts direct scientific observation in the driver's seat, and gives us a more unbiased view into the functioning of our minds.

[^1]: Star Trek (TNG) not-so-famously introduced a character "Barclay" who was obsessed with spending time in the holodeck--a ship system that could create rich virtual environments to occupy. The character name might be a subtle nod to Berkeley, or just a coincidence.

[2]: https://doi.org/10.3389/fpsyg.2014.00199 "Scene analysis in the natural environment"

[^3]: Saccades also compensate for our eyes being a kind of high pass filter, suppressing visual signals that aren't moving.


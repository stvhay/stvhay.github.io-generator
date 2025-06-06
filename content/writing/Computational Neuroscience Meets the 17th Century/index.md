+++
date = '2025-05-27T15:48:07-04:00'
draft = false
title = 'Computational Neuroscience Meets the 17th Century'
+++
*Do we live in a world of ideas?* :bulb:
<!--more-->

Descartes famously kicked off an era of Western philosophy with "Cogito, ergo sum"&mdash;an attempt to establish a basis for human existence and knowledge that assumed as little as possible. Out of this idea sprung a dualistic theory of mind and body. The theory posits that the world is composed of fundamentally two types of 'stuff': stuff that extends into the three-dimensional space (matter) and stuff that doesn't (ideas). For a long time this idea was popular, but in modern circles of philosophy, it has largely gone out of fashion in favor of materialism (one "thing"), which seems more sensible nowadays where more hard-nosed empiricism so fundamentally shapes our society.

In the 17th century, however, things weren't quite as settled. Irish philosopher George Berkeley believed the opposite of materialism&mdash;the world (including all matter) was composed only of ideas [^1]. Like modern materialists, he didn't really understand how dualism could make much sense. How does spirit interact with matter exactly? My question is: **does Berkeleyan idealism offer us any relevant perspective when we study neuroscience**?

My line of thinking is inspired by a 2014 paper[^2] that summarizes the state of neuroscience research on scene analysis&mdash;the study of how our brain turns information (materialist philosophers like the term "sense-data") into an internal representation of the world. It then argues that scene analysis is not only an incredibly hard problem, but that many of the modern ways we study this problem fail to address some very fundamental questions.

It turns out that most empirical research into scene analysis is conducted using very simplified forms&mdash;lines and basic geometric figures on simple backgrounds and neutral lighting. Arguably, this makes sense because it provides a controlled experimental environment. Unfortunately, while this research framework has given us many useful insights, the paper argues that we remain relatively stuck on how we map those insights to ecologically relevant scene analysis problems that all animals are constantly solving.[^4]

As I was reading, I was thinking about Berkeley's idealism. As I learn more about human perception in general, the more I realize that our perceptual world is far more like a Star Trek holodeck&mdash;_a constructed reality_&mdash;than some kind of more direct[^9] perception. Our lived experience is in fact deeply subjective. Not only is our brain heavily involved in numerous layers of represental transformations when processing sense-data, the resultant real-time representational model is informed by a shockingly tiny subset of the available information (neurons are expensive![^10]). So, while I don't think the world is *literally* built of ideas, it is not a totally unreasonable dialectical approach to how we materialists study perception. 

As an example, saccades are rapid eye movements that constantly shift our gaze. The movements are essential for our ability to process visual information because we physically don't have the neural bandwidth to take in all of our visual field in without heavy compression[^3]. Our brain controls where our eyes are pointed based on a mix of unconscious neural control systems tracking our head, body, and eye position; random saccade and even smaller microsaccade movements, as well as high-level task-driven signals that determine our attention. All of the high-acuity visual data we get (e.g. detail and color) comes via a surprisingly narrow field of view, and the rest we fill in with prior knowledge and expectations and much more limited peripheral visual data.

This motif recurs throughout the perceptive systems of most animals. For example, the paper discusses jumping spiders with three pairs of different kinds of eyes&mdash;only one of the pairs providing detail, and provides it as a one-dimensional vertical slit. The spider uses these eyes to scan selected areas of its visual field horizontally like a crazed dot-matrix [printer](https://youtu.be/A_vXA058EDY?t=23). Like us, the spider then assembles these samples into a three-dimensional representation of the world&mdash;the only way to explain its complex behaviors.

Bats have even more impressive autonomic systems in place to operate their neural sonar. Not only do they generate (encode) and process (decode) various sophisticated sonar signals, they focus sonic energy at targets of interest and actively adjust their sonar transmission frequencies away from those of nearby bats to reduce signal interference.

Meanwhile, some of our most famous computational vision models bear little resemblance to these attention-driven biological systems. Consider the incredibly successful ResNet image classifier. It reads entire images, breaks them down into spatio-temporal chunks, then pieces it all back together into increasingly complex groups of pixels for grouping and labeling. While there is evidence for biological neurons doing spatio-temporal filtering[^5], Resnet has no concept of three-dimensional space other than what it has memorized, no opinions on what it should be paying attention to. So, while pieces of Resnet bear some resemblance to some parts of biological brains, its overall computational architecture doesn't really have known traceability back to any biological systems. The success of ResNet has much more to do with its accomplishments as a technology than how it can specifically explain the function of biological neural systems or animal behavior[^6]&mdash;the more fundamental aim of science.

Yet scientists have the urge to apply ResNet when searching to understand the biological brain because its impressive performance might indeed reveal something more fundamental, and because it overall architecture resonates with our subjective experience of perception. The human vision system makes us feel very connected to the world. It feels like our eyes are taking it all in like a camera taking pictures or video. Therefore, it seems like the mind might process images like ResNet. It is tempting to dismiss the unconscious mechanisms of eye movement as boring biological engineering details&mdash;a distraction from the really interesting stuff that makes up human perception and thought&mdash;when the opposite (or neither!) could be true.

So while we are not literally living in Berkeleyan world of ideas, the vast bulk of our perceptive reality can be viewed as a somewhat Berkeleyan mental construct. Our brain has made us a personal holodeck[^8] very much tuned for evolutionary survival. Disbanding our own internal percetual biases first leaves us with even more mysteries. However, a major thrust of this scene analysis paper is that we really should acknowledge these mysteries and more closely examine mechanisms of animal perception to inform our research hypotheses. Doing so puts direct scientific observation in the driver's seat, and gives us a more unbiased view into the functioning of our minds.

[^1]: Star Trek (TNG) not-so-famously introduced a character "Barclay" who was obsessed with spending time in the holodeck&mdash;a ship system that could create rich virtual environments. The character name might be a subtle nod to Berkeley or just a coincidence.

[^2]: Lewicki MS, Olshausen BA, Surlykke AS, and Moss CF. (2014) Scene analysis in the natural environment. _Frontiers in Psychology_ 199 doi:[10.3389/fpsycg.2014.00199](https://doi.org/10.3389/fpsyg.2014.00199)

[^3]: Saccades also compensate for our eyes being a kind of high pass filter, suppressing visual signals that aren't moving.

[^4]: Granted, it _has_ been a bit over 10 years since this paper was published... :joy:

[^5]: This is really just one of many papers: Field D. J. (1987). Relations between the statistics of natural images and the response properties of cortical cells. _J Opt Soc Am A., Optics and image science_, 4(12), 2379–2394. doi:[10.1364/josaa.4.002379](https://doi.org/10.1364/josaa.4.002379)

[^6]: There is a really intersting paper[^7] that attempts to do this with a pretty famous Google-developed neural network that broke Internet CAPTCHAs that I am probably going to write about soon.

[^7]: George D, Lázaro-Gredilla M, Lehrach W, Dedieu A, Zhou G, and Marino J. (2025) A detailed theory of thalamic and cortical microcircuits for predictive visual inference. _Sci. Adv._ 11, eadr6698. doi:[10.1126/sciadv.adr6698](https://doi.org/10.1126/sciadv.adr6698)

[^8]: See Footnote 1.

[^9]: There is an epistemological theory based on this idea of direct access to reality called direct realism: https://en.wikipedia.org/wiki/Direct_and_indirect_realism

[^10]: I am reading [Neuron to Brain](https://www.amazon.com/Neuron-Brain-Robert-Martin/dp/1605354392) and the introductory chapters outline how the limits of physical chemistry drive to work as locally as possible, where molecular proceses can occur much more efficiently than generating expensive electrical pulse trains&mdash;especially over longer distances.